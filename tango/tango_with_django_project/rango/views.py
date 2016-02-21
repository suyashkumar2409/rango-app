from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category,Page
from rango.forms import CategoryForm
import os
# Create your views here.

def index(request):
	category_list = Category.objects.order_by('-likes')[:5]

	pages_list = Page.objects.order_by('-views')[:5]

	context = {'categories':category_list,'pages':pages_list,'numpage':len(pages_list)}

	return render(request,'index.html',context)

def about(request):
	context = {'text':"Hey!! THIS IS THE ABOUT PAGE YO!"}
	return render(request,'about.html',context)

def category(request,category_name_slug):
	context={'category_name':category_name_slug}
	try:
		category = Category.objects.get(slug = category_name_slug)

		pages = Page.objects.filter(category = category)

		category_name = category.name 

		context = {'category':category,'pages':pages,'category_name':category_name}

	
	except Category.DoesNotExist:
		pass

	return render(request,'category.html',context)

def add_category(request):
	if request.method == "POST":
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)

			return index(request)
		else:
			print form.errors

#			return render(request,'rango/add_category.html',{'form':form})

	else:
		form = CategoryForm()

		return render(request,'rango/add_category.html',{'form':form})
