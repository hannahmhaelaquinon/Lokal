from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import AutoField
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class CustomerManager(BaseUserManager):

    def create_user(self, username, firstname, lastname, phonenumber,  street, city, country, password=None, is_staff = False, is_admin = False):

        if not username:
            raise ValueError('You must provide a username')
        if not password:
            raise ValueError('You must provide a password')
        if not firstname:
            raise ValueError('You must provide a first name')
        if not lastname:
            raise ValueError('You must provide a last name')
        if not phonenumber:
            raise ValueError('You must provide a phone number')
        if not street:
            raise ValueError('You must provide a street')
        if not city:
            raise ValueError('You must provide a city')
        if not country:
            raise ValueError('You must provide a country')

        user = self.model(username=username, firstname=firstname, lastname=lastname, phonenumber=phonenumber, street=street, city=city, country=country)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.save()
        return user

    def update_user(self, username, first_name, last_name, phone_number,  street, city, country, password=None, is_staff = False, is_admin = False):

        if not username:
            raise ValueError('You must provide a username')
        if not password:
            raise ValueError('You must provide a password')
        if not first_name:
            raise ValueError('You must provide a first name')
        if not last_name:
            raise ValueError('You must provide a last name')
        if not phone_number:
            raise ValueError('You must provide a phone number')
        if not street:
            raise ValueError('You must provide a street')
        if not city:
            raise ValueError('You must provide a city')
        if not country:
            raise ValueError('You must provide a country')

        user = Customer.objects.get(username = username)
        user.set_password(password)
        user.firstname = first_name
        user.lastname = last_name
        user.phonenumber = phone_number
        user.street = street
        user.city = city
        user.country = country
        user.staff = is_staff
        user.admin = is_admin
        user.save()
        return user
    
    def create_staffuser(self, username, firstname, lastname, phonenumber,  street, city, country, password=None):
        user = self.create_user(username, firstname, lastname, phonenumber,  street, city, country, password=password, is_staff=True)
        return user
        
    def create_superuser(self, username, firstname, lastname, phonenumber,  street, city, country, password=None):
        user = self.create_user(username, firstname, lastname, phonenumber,  street, city, country, password=password, is_staff=True, is_admin=True)
        return user


class Customer(AbstractBaseUser):
    username = models.CharField(max_length = 255, primary_key = True)
    password = models.CharField(max_length = 255)
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 30)
    phonenumber = models.CharField(max_length = 11)
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    country = models.CharField(max_length = 255)
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    objects = CustomerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phonenumber', 'street', 'city', 'country']

    def __str__(self):
        return self.username

    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(seslf, app_label):
        return True
    
    @property 
    def is_staff(self):
        return self.staff

    @property 
    def is_admin(self):
        return self.admin

    class meta:
        db_table = 'Customer'


class Product(models.Model):
    item_code = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 255)
    price = models.FloatField()
    description = models.CharField(max_length = 1000)
    image = models.CharField(max_length=255, default='')

    class meta:
        db_table = 'Product'
    

class ProductType(models.Model):
    type_code = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    
    class meta:
        db_table = 'ProductType'
    
    

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=256)
    total_price = models.FloatField()

    class meta:
        db_table = 'Cart'


class CartItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_code = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    cart_id = models.IntegerField()
  

    class meta:
        db_table = 'CartItem'
 