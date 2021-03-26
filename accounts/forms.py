from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import inlineformset_factory # allows to create multiple copies of one form 
from .models import *


class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user'] # exclude user - customers can modify only their own profile but not their user model
		
		# Here you can add a styles and aditional attributes to all form fields
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'phone':forms.TextInput(attrs={'class': 'form-control'}),
			'email':forms.EmailInput(attrs={'class': 'form-control'}),
			'profile_pic':forms.FileInput(attrs={'class': 'form-control-file'}),
		}
		labels = {
			'profile_pic': 'Profile Picture'
		}


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['product','status','note']

		widgets = {
			'product': forms.Select(attrs={'class': 'form-control w-100'}),
			'status': forms.Select(attrs={'class': 'form-control w-100'}),
			'note': forms.TextInput(attrs={'class': 'form-control w-100', 'placeholder':'Note'}),
		}

# Replicate django user creation form and customize data
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


# Form class to use in inlineformset (allows to create multiple copies of one form )
class OrderFormSet(ModelForm):	
	class Meta:
		model = Order
		fields = ['product', 'status', 'note']


# Formset is a layer of abstraction to work with multiple forms on the same page (in one form)
# inlineformset_factory(parent, child, form_fields, extra=create 6 forms, can_delete=display delete checkbox)
OrderFormSet = inlineformset_factory(Customer, Order, form=OrderFormSet, extra=6, can_delete=False,
		widgets = {
			'product': forms.Select(attrs={'class': 'form-control w-100 mb-3 mt-1'}),
			'status': forms.Select(attrs={'class': 'form-control w-100 mb-3 mt-1'}),
			'note': forms.TextInput(attrs={'class': 'form-control w-100 mb-3 mt-1', 'placeholder':'Note'}),
		})