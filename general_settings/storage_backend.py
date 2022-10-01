from .models import StorageBuckets
from django.db.models.fields.files import FieldFile
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


def activate_storage_type():
    try:
        return StorageBuckets.objects.get(pk=1).storage_type
    except:
        return True

def get_bucket_name():
    try:
        return StorageBuckets.objects.get(pk=1).bucket_name
    except:
        return None

def get_access_key():
    try:
        return StorageBuckets.objects.get(pk=1).access_key
    except:
        return None

def get_secret_key():
    try:
        return StorageBuckets.objects.get(pk=1).secret_key
    except:
        return None

def local_storage(instance, filename):
    return "application/%s/%s" % (instance.application.team.title, filename)


def s3_storage(backet_name:str, access_key:str, secret_key:str, default_acl:None):
    # return S3BotoStorage(s3_storage(
    #         backet_name=get_bucket_name(), 
    #         access_key=get_access_key(), 
    #         secret_key=get_secret_key()
    #     ))
    return dict(backet_name=backet_name, access_key=access_key, secret_key=secret_key, default_acl=None)


class S3Bucket(S3Boto3Storage):
    def __init__(self, backet_name=None, access_key=None, secret_key=None, default_acl=None):

        super(S3Bucket, self).__init__(
            backet_name= get_bucket_name() if backet_name is None else backet_name, 
            access_key= get_access_key() if access_key is None else access_key, 
            secret_key= get_secret_key() if secret_key is None else secret_key,  
            default_acl = None if default_acl is None else default_acl, 
        )


class StorageBackend(FieldFile):
    def __init__(self, instance, field, name):
        super(StorageBackend, self).__init__(instance, field, name)
        if instance.STORAGE == False:
            self.storage = s3_storage()
        else:
            self.storage = local_storage(instance, name)



class DynamicStorageField(models.FileField):
    attr_class = StorageBackend

    def pre_save(self, model_instance, add):
        if model_instance.STORAGE == False:
            storage = s3_storage()
        else:
            storage = local_storage()
        self.storage = storage
        self.image.storage = storage
        # self.file.storage = storage

        file = super(DynamicStorageField, self).pre_save(model_instance, add)
        return file






def general_file_directory():
    print('boto')
    # if activate_s3_bucket() == True:
    #     return S3BotoStorage(s3_storage(
    #         backet_name=get_bucket_name(), 
    #         access_key=get_access_key(), 
    #         secret_key=get_secret_key()
    #     ))
    # else:
    #     return local_file_storage()
