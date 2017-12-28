from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
NAME_REGEX = re.compile(r'[a-zA-Z]+')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
# models
class UserManager(models.Manager):
    def validate(self, post_data):
        errors = []
        p = post_data
        first_name, last_name, email, password, cpassword = p['first_name'], p['last_name'], p['email'], p['password'], p['cpassword']
        
        if not first_name or not last_name or not email or not password or not cpassword:
            errors.append("All fields are required")
        else:
            if len(first_name) < 2 or len(last_name) < 2 or not re.match(NAME_REGEX, first_name) or not re.match(NAME_REGEX, last_name):
                errors.append("Invalid names")            
            if not re.match(EMAIL_REGEX, email):
                errors.append("Invalid email") 
            if len(password) <8:
                errors.append("Invalid password!")
            elif password != cpassword:
                errors.append("Passwords must match")
        
        if not errors:
            if self.filter(email=email):
                errors.append("email already in use")
            else:     
                hash_in = bcrypt.hashpw(password.encode(), bcrypt.gensalt())                
                return self.create(
                    firstname = first_name,
                    lastname = last_name,
                    email = email,
                    password = hash_in
                )    
        return errors

    def validate_login(self, login_data):
        errors = []
        email, password = login_data['email'], login_data['password']
        if not email or not password:
            errors.append("All fields are required")
        else:
            if not re.match(EMAIL_REGEX, email) or len(password) <8:
                errors.append("Invalid fields") 
            #  existing email check
            else:
                persons = self.filter(email=email)
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

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __str__(self):
        return "<User object: {} {} {}>".format(self.firstname, self.lastname, self.email, self.password)
