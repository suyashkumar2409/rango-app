from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
import os
# Create your views here.

def index(request):


	category_list = Category.objects.order_by('-likes')

	pages_list = Page.objects.order_by('-views')[:5]

	context = {'user':request.user, 'categories':category_list,'pages':pages_list,'numpage':len(pages_list)}


####### SETTING UP COUNTER USING COOKIES
	visits = int(request.session.get('visits','1'))
	if not visits:
		visits = 1

	context['visits'] = visits
	reset_last_visit = False

	last_visit = request.session.get('last_visit')

	if last_visit:

		last_visit_time = datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")
		if (datetime.now()-last_visit_time).days>0:
			visits = visits+1
			reset_last_visit = True

	else:
		reset_last_visit = True

	response = render(request,'index.html',context)


	if reset_last_visit is True:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = str(visits)
	#request.session['visits'] = str(1)

	return response

def about(request):
	context = {'text':"Hey!! THIS IS THE ABOUT PAGE YO!"}
	return render(request,'about.html',context)

"""
def register(request):

	registered = False

	if request.method == 'POST':

		user_form = UserForm(data = request.POST)
		userprof_form = UserProfileForm(data = request.POST)

		if user_form.is_valid() and userprof_form.is_valid():
			user = user_form.save(commit = False)

			user.set_password(user.password)
			user.save()


			userprof = userprof_form.save(commit = False)
			userprof.user = user

			if 'picture' in request.FILES:
				userprof.picture = request['picture']

			userprof.save()

			registered = True

		else:
			print (user_form.errors)
			print (userprof_form.errors)

	else:
		user_form = UserForm()
		userprof_form = UserProfileForm()


	return render(request,'register.html',{'user_form':user_form,'userprof_form':userprof_form,'registered':registered})


def user_login(request):

	if request.method=="POST":
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username = username , password = password)

		if user:
			if user.is_active:

				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse("Your Rango account has been disabled. Please Contact Admin")
		else:

			print("Invalid Login Details for "+username)
			return HttpResponse("Invalid Login Details for "+username)

	else:

		return render(request,'login.html',{})

@login_required
def user_logout(request):
	logout(request)

	return HttpResponseRedirect('/rango/')
"""
@login_required
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

@login_required
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

@login_required
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

@login_required
def track_url(request,page_id):
	try:
		page = Page.objects.get(id = page_id)
		page.views = page.views+1
		page.save()

		return HttpResponseRedirect(page.url)
	except:
		return HttpResponseRedirect('/rango/')
