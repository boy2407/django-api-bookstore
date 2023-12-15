from django.shortcuts import render
from .models import Category
def sidebar(request):
	categories = Category.objects.all()
	context = {
		"cat":categories
	}
	return context
def header(request):
	categories = Category.objects.all()
	context = {
		"cat":categories
	}
	return context



	