from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
class Category(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 150, unique=True ,db_index=True)
	icon = models.FileField(upload_to = "category/%y/%m")
	create_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now_add = True)

	class Meta:
		verbose_name_plural = 'categories'
	def __str__(self):
		return self.name

class Writer(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length=150, unique=True ,db_index=True)
	bio = models.TextField()
	pic = models.FileField(upload_to = "writer/%y/%m")
	create_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.name

class Book(models.Model):
	writer = models.ForeignKey(Writer, on_delete = models.CASCADE)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)

	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length=100, db_index=True)
	price = models.IntegerField()
	pricesale = models.IntegerField()
	stock = models.IntegerField()

	coverpage = models.FileField(upload_to = "coverpage/%y/%m")
	image = models.FileField(upload_to = "images/%y/%m")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	totalreview = models.IntegerField(default=1)
	totalrating = models.IntegerField(default=5)
	status = models.IntegerField(default=0)
	description = models.TextField()
	class Meta:
		verbose_name_plural = 'Books'

	def __str__(self):
	    return self.name

	def get_absolute_url(self):
		return reverse('list-category', args=[self.slug])


class Review(models.Model):
	customer = models.ForeignKey(User, on_delete = models.CASCADE)
	book = models.ForeignKey(Book, on_delete = models.CASCADE)
	review_star = models.IntegerField()
	review_text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

class Slider(models.Model):
	title = models.CharField(max_length=150)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	slideimg = models.FileField(upload_to = "slide/")

	def __str__(self):
		return self.title

