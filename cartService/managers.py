from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    # def create_user(self, email, username, password=None):
    #     if not email:
    #         raise ValueError('The Email field must be set')
    #     user = self.model(email=self.normalize_email(email), username=username)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create_superuser(self, email, username,password=None):
        # user = self.create_user(email, username,password=password)
        # user.is_admin = True
        # user.is_superuser = True
        # user.save(using=self._db)
        # return user
        #
        # or 
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        is_staff = extra_fields.pop('is_staff', False)
        is_superuser = extra_fields.pop('is_superuser', False)
        is_admin = extra_fields.pop("is_admin", False)
        user = self.model(email=self.normalize_email(email), username=username, **extra_fields)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username,password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)
        
        return self.create_user(email, password, username, **extra_fields)

  

        


        