from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class TresPlayerManager(BaseUserManager):
    def create_user(self, telegram_id, first_name, password=None):
        if not telegram_id:
            raise ValueError("User must have telegram_id")
        user = self.model(telegram_id=telegram_id, first_name=first_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, first_name, password=None):
        user = self.create_user(telegram_id, first_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 

# User model
class TresPlayer(AbstractBaseUser, PermissionsMixin):
    # User account info
    telegram_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    # User game data
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    played_rounds = models.IntegerField(default=0)
    victory_rounds = models.IntegerField(default=0)
    defeat_rounds = models.IntegerField(default=0)
    ranking_place = models.IntegerField(default=100)

    # Other
    is_agreed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = ['first_name']

    objects = TresPlayerManager()

    def __str__(self):
        return f"{self.first_name} ({self.telegram_id})"
