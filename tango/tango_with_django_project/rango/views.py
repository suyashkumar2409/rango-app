from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm
import os
# Create your views here.

def index(request):
	category_list = Category.objects.order_by('-likes')

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

		context = {'category':category,'pages':pages,'category_name':category_name,'category_name_slug':category_name_slug}

	
	except Category.DoesNotExist:
		doesntstr = "This Category does not Exist!!"
		returnstr = "<a href='/rango/'>Return</a>"
		return HttpResponse(doesntstr+returnstr)

	return render(request,'category.html',context)

def add_category(request):
	if request.method == "POST":
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)

			return index(request)
		else:
			print (form.errors)

			return render(request,'add_category.html',{'form':form})

	else:
		form = CategoryForm()

		return render(request,'add_category.html',{'form':form})

def add_page(request,category_name_slug):
	try:
		cat = Category.objects.get(slug = category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid:
			page = form.save(commit = False)
			page.category = cat
			page.views=0
			page.save()

			return category(request,category_name_slug)

		else:
			print(form.errors)
			return render(request,'add_page.html',{'form':form,'category':cat,'category_name_slug':category_name_slug})
		
	else:
		form = PageForm()

	return render(request,'add_page.html',{'form':form,'category':cat,'category_name_slug':category_name_slug})

