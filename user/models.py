from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		"""
		Creates and returns a user with an email, name, and password.
		"""
		if not email:
			raise ValueError('The Email field must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password) 
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		"""
		Creates and returns a superuser with an email, name, and password.
		"""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)
		if password is None:
			raise ValueError('Superuser must have a password')
		
		return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	"""
	Custom user model that uses email as the unique identifier.
	"""
	email = models.EmailField(unique=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now=True) 
	is_active = models.BooleanField(default=True)

	objects = UserManager()

	USERNAME_FIELD = 'email' 
	REQUIRED_FIELDS = ['name'] 

	def tokens(self):
		"""
		Generates JWT tokens for the user.
		"""
		refresh = RefreshToken.for_user(self)
		refresh['user_name'] = self.email
		refresh['user_id'] = str(self.id)
		return {
			'RefreshToken': str(refresh),
			'AccessToken': str(refresh.access_token)
		}

	def __str__(self):
		return self.email
