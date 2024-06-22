from django.db import models
from django.utils import timezone
from cryptography.fernet import Fernet
import random
from .utils import generate_fernet_key  # Import the public_key function

class Register_Detail(models.Model):
	email = models.EmailField(max_length=50,unique=True)
	name = models.CharField(max_length=50)
	fname = models.CharField(max_length=50)
	lname = models.CharField(max_length=50)
	address = models.CharField(max_length=50)
	mobile = models.CharField(max_length=20)
	password = models.CharField(max_length=50)
	gender = models.CharField(max_length=50,null=True, blank=True)
	age = models.CharField(max_length=50,null=True, blank=True)
	country = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	zip = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField(null=True, blank=True)
	encrypted_description = models.TextField(null=True, blank=True)
	description_key = models.CharField(max_length=44, null=True, blank=True)  # 44 characters for URL-safe base64 encoding
	user_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE)
	gender = models.CharField(max_length=50,null=True, blank=True)
	age = models.CharField(max_length=50,null=True, blank=True)
	date = models.DateField('Posted Date', default=timezone.now())

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.id and not self.description_key:
		    self.description_key = generate_fernet_key()

		if self.description:
		    fernet_key = self.description_key.encode()
		    cipher = Fernet(fernet_key)
		    encrypted_description = cipher.encrypt(self.description.encode())
		    self.encrypted_description = encrypted_description.decode()

		super().save(*args, **kwargs)
class Post_Feedback(models.Model):
	like_post = models.CharField(max_length=50,null=True,blank=True)
	report_post = models.CharField(max_length=50,null=True,blank=True)
	user_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE)
	post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
	date = models.DateField('Posted Date',default=timezone.now())
	def __str__(self):
		return self.post_id.title
	def publish(self):
		self.date = timezone.now()
		self.save()
class Feedback(models.Model):
	post_id =  models.ForeignKey(Post, on_delete=models.CASCADE)
	user_id =  models.ForeignKey(Register_Detail, on_delete=models.CASCADE)
	comment = models.CharField(max_length=30)
	date = models.DateField('Posted Date',default=timezone.now())
	def __str__(self):
		return self.post_id.title
	def publish(self):
		self.date = timezone.now()
		self.save()
class Women_Right(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField(max_length=2000)
	image = models.FileField('Upload Image',upload_to='documents/',null=True)
	def __str__(self):
		return self.title
class NGO(models.Model):
	name = models.CharField(max_length=50)
	number = models.CharField(max_length=15)
	def __str__(self):
		return self.name
class FollowUser(models.Model):
	user_id =  models.ForeignKey(Register_Detail, on_delete=models.CASCADE)
	follow_id = models.IntegerField(null=True)
	status = models.CharField(max_length=30,null=True)
	def __str__(self):
		return self.status
	def publish(self):
		self.date = timezone.now()
		self.save()
