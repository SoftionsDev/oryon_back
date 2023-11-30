from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.db import models

from principal.base_models import BaseModel
from users.constants import GoalTypes


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    code = models.CharField(max_length=100, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    position = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    groups = models.ManyToManyField(Group, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'

    @property
    def is_admin(self):
        return self.groups.filter(name='admin').exists()

    @property
    def is_manager(self):
        return self.groups.filter(name='manager').exists()


class Commercial(BaseModel):

    GOAL_TYPES_CHOICES = (
        ('D', GoalTypes.DAILY),
        ('M', GoalTypes.MONTHLY),
        ('Y', GoalTypes.YEARLY),
    )

    user: User = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='commercial'
    )
    manager: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commercials', null=True, blank=True
    )
    goal_type = models.CharField(max_length=100, choices=GOAL_TYPES_CHOICES)
    goal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "commercials"

    def __str__(self):
        return self.user.email
