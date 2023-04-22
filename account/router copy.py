from django.db import connections
from django.apps import apps


class MerchantRouter:
    def _get_schema_name(self, request=None, model=None):
        """Get the schema name based on the request object and model being accessed."""
        if model is not None and 'merchant_id' in [field.name for field in model._meta.fields]:
            # If the model has a `merchant_id` field, assume it belongs to a tenant
            if hasattr(request, 'tenant') and request is not None and request.tenant is not None:
                return connections[request.tenant].schema_name
        else:
            # Otherwise, assume it belongs to the public schema
            if hasattr(request, 'parent_site') and request is not None and request.parent_site is not None:
                return "public"
        return None

    def db_for_read(self, model, **hints):
        schema_name = self._get_schema_name(model=model)
        if schema_name is None:
            return None
        return schema_name

    def db_for_write(self, model, **hints):
        schema_name = self._get_schema_name(model=model)
        if schema_name is None:
            return None
        return schema_name

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        schema_name = self._get_schema_name(model=apps.get_model(app_label, model_name))
        if schema_name == 'public':
            # Only allow models in the public schema to be migrated on the default database
            return connections.schema_name == 'public'
        elif hasattr(connections, 'schema_name') and connections.schema_name.startswith('merchant_'):
            # For non-default databases, only allow models that have a matching schema_name to be migrated
            return db == connections.schema_name
        else:
            return None


