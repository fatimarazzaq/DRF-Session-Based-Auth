from django.db import models 
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if self.model.objects.filter(username=username).exists():
            raise ValueError("The username you have entered already exists")
        user = self.model(email=self.normalize_email(email),username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        user = self.create_user(
            username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_staff=True
        user.is_admin=True
        user.save()
        return user


class UserAccount(AbstractBaseUser):
    username = models.CharField(max_length=255,verbose_name="Username",unique=True)
    email = models.EmailField(max_length=255,verbose_name="Email",unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    objects = UserAccountManager()
    USERNAME_FIELD=  'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin
    

