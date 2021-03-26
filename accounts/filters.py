import django_filters
from django_filters import DateFilter, CharFilter, ModelChoiceFilter, NumberFilter
from django import forms
from django.forms import TextInput, DateInput, Select
from .models import *


class OrderFilter(django_filters.FilterSet):
    # Add custom filter fields
	start_date = DateFilter(
		field_name="date_created",
		lookup_expr='gte',
		label='Start Date',
		widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MM/DD/YYYY'})
	)
	end_date = DateFilter(
		field_name="date_created",
		lookup_expr='lte',
		label='End Date',
		widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MM/DD/YYYY'})
	)
	note = CharFilter(
		field_name='note',
		lookup_expr='icontains',
		label='Note Contains', 
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Note'})
	)

	# override constructor to add classes to filter (for Meta form class fields : 'product','status)
	def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
		super(OrderFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
		self.filters['product'].field.widget.attrs.update({'class': 'custom-select'})
		self.filters['status'].field.widget.attrs.update({'class': 'custom-select'})


	class Meta:
		model = Order
		fields = '__all__'
		exclude = ['customer', 'date_created']



class CustomerFilter(django_filters.FilterSet):
	def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
		super(CustomerFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
		self.filters['id'].field.widget.attrs.update({'class': 'form-control'})
		self.filters['name'].field.widget.attrs.update({'class': 'form-control'})
		self.filters['phone'].field.widget.attrs.update({'class': 'form-control'})
		self.filters['email'].field.widget.attrs.update({'class': 'form-control', 'min':'1'})


	class Meta:
		model = Customer
		fields = ['id', 'name', 'phone', 'email']
        # Override filter char fields - replace 'exact' with 'contains' value
		filter_overrides =	{
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.EmailField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
		}



class ProductFilter(django_filters.FilterSet):
	# Get tags 
	tags =  ModelChoiceFilter(
		field_name='tags',
		queryset=Tag.objects.all(),
		label='Tags', 
		widget=forms.Select(attrs={'class': 'form-control'})
	)
	price_min = NumberFilter(
		field_name='price',
		lookup_expr='gte',
		label='Price Min',
		widget=forms.TextInput(attrs={'class': 'form-control'})
	)
	price_max = NumberFilter(
		field_name='price',
		lookup_expr='lte',
		label='Price Max',
		widget=forms.TextInput(attrs={'class': 'form-control'})
	)

	def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
		super(ProductFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
		self.filters['name'].field.widget.attrs.update({'class': 'form-control'})
		self.filters['category'].field.widget.attrs.update({'class': 'form-control'})


	class Meta:
		model = Product
		fields = ['id', 'name', 'price_min', 'price_max', 'category','tags']
       	
		filter_overrides =	{
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
		}