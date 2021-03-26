from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages # default flash msg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage

from .models import *
from .forms import *
from .filters import *
from .decorators import *


@unauthenticated_user
def registerPage(request):
	# This code was moved code moved to decorators/ uncomment if not using @unauthenticated_user
	# if request.user.is_authenticated:
	# 	return redirect('home')
	
	form = CreateUserForm() # Customized UserCreationForm (forms.py)
	if request.method == 'POST':
		form = CreateUserForm(request.POST) 
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			# # This code was moved to signals / uncomment if not using signals 
			# group = Group.objects.get(name='customer') # get customer group object
			# user.groups.add(group) # add group to customer profile
			# # Apart of creating user object create related profile(customer object) 
			# Customer.objects.create(
			# 	user=user,
			# 	name=user.username,
			# 	) 

			messages.success(request, 'Account was created for ' + username)
			return redirect('login')		
	
	context = {'form':form}
	return render(request, 'accounts/register.html', context)



@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')
		# Authenticate user
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user) # Default django login method
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)



def logoutUser(request):
	logout(request)
	return redirect('login')



@login_required(login_url='login') # Login decorator must go first
@admin_only # Custom decorator, modified @allowed_users, changes redirect for customers
def home(request):
	customers = Customer.objects.all().order_by('-pk')
	total_customers = customers.count()

	orders = Order.objects.all().order_by('-pk')
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	out_for_delivery = orders.filter(status='Out for delivery').count()
	pending = orders.filter(status='Pending').count()

	# Add custom Customer model search filter
	customer_filter = CustomerFilter(request.GET, queryset=customers) 
	customers = customer_filter.qs

	# Paginators
	p_orders = Paginator(orders,10)	 # create orders paginator & set orders per page
	page_num = request.GET.get('o_page', 1) # get page number from url param or set page num as 1
	page_orders = p_orders.get_page(page_num)

	p_customers = Paginator(customers,10)
	page_num_c = request.GET.get('c_page', 1)
	page_customers = p_customers.get_page(page_num_c)

	# To use paginator replace 'orders':orders with 'orders':page_orders
	context = {
		'orders':page_orders,
		'orders_pages_total':p_orders.num_pages, 
		'customers':page_customers,
		'customers_pages_total':p_customers.num_pages, 
		'total_orders':total_orders,
		'delivered':delivered,
		'out_for_delivery':out_for_delivery,
		'pending':pending,
		'customer_filter':customer_filter
	}
	return render(request, 'accounts/dashboard.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all().order_by('-pk') # Get customers orders
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	out_for_delivery = orders.filter(status='Out for delivery').count()
	pending = orders.filter(status='Pending').count()

	# Add custom Order model search filter
	filter = OrderFilter(request.GET, queryset=orders) 
	orders = filter.qs

	p_orders = Paginator(orders,10)
	page_num = request.GET.get('page', 1)
	page = p_orders.get_page(page_num)

	context = {
		'orders':page,
		'total_orders':total_orders,
		'delivered':delivered,
		'out_for_delivery':out_for_delivery,
		'pending':pending,
		'paginator_list':page,
		'paginator_pages_total':p_orders.num_pages,
		'filter':filter,
	}
	return render(request, 'accounts/user.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer']) # edit account (customer only)
def accountSettings(request):
	# Get profile(Customer model) of authenticated customer
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		# Add request.FILES, to upload files that come from the request
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	# Add custom Order model search filter
	product_filter = ProductFilter(request.GET, queryset=products) 
	products = product_filter.qs

	# Paginator
	p_products = Paginator(products,10)
	page_num = request.GET.get('page', 1)
	page_products = p_products.get_page(page_num)

	return render(request, 'accounts/products.html', {
		'products':page_products, 
		'paginator_list':page_products,
		'paginator_pages_total':p_products.num_pages,
		'product_filter':product_filter
	})



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	# parent.child_set.all() query customer child object
	orders = customer.order_set.all().order_by('-pk')
	order_count = orders.count()

	# Add custom Order model search filter
	filter = OrderFilter(request.GET, queryset=orders) 
	orders = filter.qs
	
	# Paginator
	p_orders = Paginator(orders,10)
	page_num = request.GET.get('page', 1)
	page_orders = p_orders.get_page(page_num)
	
	context = {
		'customer':customer,
		'orders':page_orders,
		'paginator_list':page_orders,
		'paginator_pages_total':p_orders.num_pages, 
		'order_count':order_count,
		'filter':filter,
	}
	return render(request, 'accounts/customer.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	customer = Customer.objects.get(id=pk)
	# Use formset - pass customer instance (queryset=Order.objects.none() - hides already existing orders for given instance) 
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)  

	if request.method == 'POST':
		# Pass form post request data & customer instance into formset
		formset = OrderFormSet(request.POST, instance=customer) 
		if formset.is_valid():
			formset.save()
			return redirect('/')
			# return redirect(request.path_info) # Redirect to the same page

	context = {'form':formset, 'customer':customer}
	return render(request, 'accounts/order_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	# Added order to display customer info
	context = {'form':form, 'order':order}
	return render(request, 'accounts/update_order_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')
	return redirect('/')



# Custom error views will work only if debug=False (look settings.py)
def error_404(request, exception):
	data = {}
	return render(request,'404.html', data)


def error_403(request, exception):
    return render(request,'403.html')


def error_500(request, *args, **argv):
    return render(request,'500.html', status=500)