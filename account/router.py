from django.db import connections
from django.apps import apps


class MerchantRouter:
    def db_for_read(self, model, **hints):
        # Use the merchant_id attribute in the request to route the database operation
        merchant_id = getattr(connections["default"], "tenant_id", None)
        if merchant_id:
            return f"merchant_{merchant_id}"
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Allow migrations for all apps in the "public" schema
        if db == "public":
            return True

        # Allow migrations for the current tenant schema only
        merchant_id = getattr(connections["default"], "merchant_id", None)
        if merchant_id:
            return db == f"merchant_{merchant_id}"
        return False
