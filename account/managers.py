from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, short_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The given email field is required"))
        if not password:
            raise ValueError(_("You must set a valid password"))

        email = self.normalize_email(email)
        user = self.model(email=email, short_name=short_name, **extra_fields)
        user.is_active = True
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, short_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, short_name, password, **extra_fields)
