from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    # Need a new model manager since we removed the username field

    use_in_migrations = True

    # all-auth creates our users, but createsuperuser will call this
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # for creating regular users - probably won't need
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    # needs fields to contain everything associated with a profile page
    username = None
    email = models.EmailField(('email address'), unique=True)
    has_active_request = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()


class Request(models.Model):
    # need a field that maps the request to the user that wrote it (one-to-one relationship)
    title = models.CharField(max_length=200)  # the title of the request
    location = models.CharField(max_length=200)  # the location of the tutee (as specified by the tutee)
    pub_date = models.DateTimeField('date published',max_length=100)  # when it was published
    description = models.CharField(max_length=1000)  # a description written by the tutee
    user = models.CharField(max_length=100) # email goes here - the unique ID
    tutors = models.ManyToManyField(User) # tutors that have offered help will be added onto this
    def __str__(self):
        return self.title


class Conversation(models.Model):
    # need a field that maps the conversation to both users
    # need a field that tracks the list of sent messages
    pass

