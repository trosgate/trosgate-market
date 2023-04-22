from django.db import connections


class MerchantRouter:

    def _get_schema_name(self, request=None):
        """Get the schema name based on the request object."""

        if hasattr(request, 'tenant') and request is not None and request.tenant is not None:
            print('tenanto ::', connections[request.tenant].schema_name)
            print('merchanto ::', connections[request.merchant].schema_name)
            return connections[request.tenant].schema_name

        elif hasattr(request, 'parent_site') and request is not None and request.parent_site is not None:
            return "public"
        else:
            return None

    def db_for_read(self, model, **hints):
        schema_name = self._get_schema_name()
        if schema_name is None:
            return None
        return schema_name

    def db_for_write(self, model, **hints):
        schema_name = self._get_schema_name()
        if schema_name is None:
            return None
        return schema_name

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # return True
        schema_name = self._get_schema_name()
        if schema_name == 'public':
            # Only allow models in the public schema to be migrated on the default database
            return connections.schema_name == 'public'
        elif hasattr(connections, 'schema_name') and connections.schema_name.startswith('merchant_'):
            # For non-default databases, only allow models that have a matching schema_name to be migrated
            return db == connections.schema_name
        else:
            return None

    def create_tenant_schema(self, tenant):
        schema_name = f'merchant_{tenant.id}'

        with connections.cursor() as cursor:
            # Check if the schema already exists
            cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema_name}'")
            if not cursor.fetchone():
                # Create the new schema
                cursor.execute(f"CREATE SCHEMA {schema_name}")

        return schema_name

