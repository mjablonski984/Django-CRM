from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

# If user is not authenticated(not logged in)redirect to home, else call original function
def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home') 
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

# decorator takes an parameters beyond view_func, one layer added
def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			# check if user is assigned to groups and get the first group
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name 
			# If group is in array of allowed groups call the original function
			if group in allowed_roles: 
				return view_func(request, *args, **kwargs)
			else:
				# return HttpResponse('Forbidden', status=403)
				# use exceptions instead of httpResponse if you want to display your custom 403 page
				raise PermissionDenied()
		return wrapper_func
	return decorator


# modified allowed_users, use on admin-only home dashboard view - changes redirect route 
def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			return redirect('user-page') # if customer - redirect to customer dashboard

		if group == 'admin':
			return view_func(request, *args, **kwargs)  # if admin - run original function (go to home admin panel)

	return wrapper_function