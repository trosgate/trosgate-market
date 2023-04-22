
class MerchantRouter:
    def db_for_read(self, model, **hints):
        if hasattr(model, 'merchant'):
            return 'merchant_' + str(hints.get('instance').merchant.id)
        return 'default'
    
    def db_for_write(self, model, **hints):
        if 'merchant' in [field.name for field in model._meta.fields]:
            return 'merchant_' + str(hints.get('instance').merchant.id)
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):        
        if 'merchant' in [field.name for field in hints.get('model', None)._meta.fields]:
            return db == 'merchant'
        return db == 'default'