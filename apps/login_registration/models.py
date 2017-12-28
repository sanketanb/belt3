from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

# models

class UserManager(models.Manager):
    def validate(self, post_data):
        errors = []
        p = post_data
        name, username, password, cpassword, date_hired = p['name'], p['username'], p['password'], p['cpassword'], p['date_hired']
        
        if not name or not username or not password or not cpassword or not date_hired:
            errors.append("All fields are required")
        else:
            if len(name) < 3 or len(username) < 3:
                errors.append("Invalid names")            
            if len(password) <8:
                errors.append("Invalid password!")
            elif password != cpassword:
                errors.append("Passwords must match")
        
        if not errors:
            if self.filter(username=username):
                errors.append("username already in use")
            else:     
                hash_in = bcrypt.hashpw(password.encode(), bcrypt.gensalt())                
                return self.create(
                    name = name,
                    username = username,
                    password = hash_in,
                    date_hired = date_hired
                )    
        return errors

    def validate_login(self, login_data):
        errors = []
        username, password = login_data['username'], login_data['password']
        if not username or not password:
            errors.append("All fields are required")
        else:
            if len(username) <3 or len(password) <8:
                errors.append("Invalid fields") 
            #  existing username check
            else:
                persons = self.filter(username=username)
                if len(persons) == 0:
                    errors.append("Please register")
                else:
                    hash1 = persons[0].password
                    if bcrypt.checkpw(password.encode(), hash1.encode()) == True:
                        # print ("password match")
                        # taking only the first user from the filtered persons, index=0
                        user = persons[0]
                        return user
                    else:
                        errors.append("Invalid password")
        return errors

class ProductManager(models.Manager):
    def validate_new_product(self, product_data, id):
        errors = []
        product_name = product_data['product_name']
        if not product_name:
            errors.append("Field is required! Cannot be empty!!")
        else:
            if len(product_name) < 4:
                errors.append("Invalid item/product!")
            if not errors:
                if self.filter(product_name=product_name):
                    errors.append("Product already created")
                else:                
                    return self.create(
                        product_name = product_name,
                        user = User.objects.get(id=id)
                    )    
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    date_hired = models.DateField()
    objects = UserManager()
    # def __str__(self):
    #     return "<User object: {} {} {}>".format(self.name, self.username, self.password)

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    # one User can create many products
    user = models.ForeignKey(User, related_name="products")
    created_at = models.DateTimeField(auto_now_add = True)
    objects = ProductManager()

class Wish(models.Model):
    # one Product can belong to many user's wishes
    product = models.ForeignKey(Product, related_name="wishes")
    # one User can have many wishes
    user = models.ForeignKey(User, related_name="wishes")
    created_at = models.DateTimeField(auto_now_add = True)