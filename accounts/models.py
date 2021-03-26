from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# blank: Validation-related - It will be used during forms validation, when calling form.is_valid(). True means empty values are allowed,
#  while False means the form will generate an error if not provided.

# null: Database-related - defines if a given database column will accept null values or not.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) # Link to User model and delete when user is deleted
    name = models.CharField(max_length=50, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Please use correct phone number format:(+)999999999. Max15 digits allowed.") # not a model field ! 
    phone = models.CharField(max_length=50, null=True, validators=[phone_regex])
    email = models.EmailField(null=True)
    profile_pic = models.ImageField(default="default_user.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    # Override save method to delete old image when uploading a new one (alt. use signals) 
    def save(self, *args, **kwargs):
        try:
            this = Customer.objects.get(id=self.id)
            if this.profile_pic != self.profile_pic:
                this.profile_pic.delete()
        except: pass
        super(Customer, self).save(*args, **kwargs)



class Tag(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    CATEGORY = (
            ('Hiking', 'Hiking'),
            ('Camping', 'Camping'),
            ('Cycling', 'Cycling'),
            ) 

    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag) # Many-to-many relation (uses an intermediary model that holds two ForeignKey fields pointed at the two sides of the relation).

    def __str__(self):
        return self.name
    


class Order(models.Model):
    STATUS = (
            ('Pending', 'Pending'),
            ('Out for delivery', 'Out for delivery'),
            ('Delivered', 'Delivered'),
            )
    # On foreign keys - set column value to null when customer/product is deleted
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL) 
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS)
    note = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'Order #{self.id} - {self.product.name}'