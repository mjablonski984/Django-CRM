from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import Customer
import os

# For signals to work override 'ready' method in apps.py  OR  in __init__.py add: default_app_config = 'accounts.apps.AccountsConfig')

# Create (Customer) profile for newly created user .
@receiver(post_save,sender=User)
def customer_profile(sender, instance, created, **kwargs):
    # send when user is created (created == False - works only on update)
	if created:
			# Add 'admin' group to superuser created via shell or fixtures(called to populate db). Groups must be created in admin panel,shell or  fixtures
		if instance.is_staff:
			group = Group.objects.get(name='admin')
			instance.groups.add(group)
		else:
			# Add 'customer' group to each user that doesn't have 'staff' status (look django user in admin panel) and isn't assigned to 'admin' group.
			group = Group.objects.get(name='customer')
			instance.groups.add(group)
			# Link current created user(instance) with this new Customer object (only users assigned to 'customer' group)
			Customer.objects.create(
				user=instance,
				name=instance.username,
				email=instance.email,
				)
# post_save.connect - can be used in place of receiver decorator
# post_save.connect(customer_profile, sender=User)


# User Pre Save - Format User model data before saving
@receiver(pre_save,sender=User)
def format_customer_data(sender, instance, **kwargs):
	instance.email = instance.email.lower()
	instance.first_name = instance.first_name.title()
	instance.last_name = instance.last_name.title()


# Customer Pre Save - Format Customer model data before saving
@receiver(pre_save,sender=Customer)
def format_user_data(sender, instance, **kwargs):
	instance.name = instance.name.title()
	instance.email = instance.email.lower()
	

# Customer Post Save
@receiver(post_save,sender=Customer)
def format_user_data(sender, instance, created, **kwargs):
	if created == False:
		# When email in Customer Profile is updated, update email in linked User model
		instance.user.email = instance.email.lower()
		instance.user.save()
