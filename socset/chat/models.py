from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from markdown_deux import markdown

from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User


class Chat(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	message = models.TextField()
	datamessage = models.DateTimeField(auto_now=True, 
									auto_now_add=False)

	def __str__(self):
		return str(self.user)