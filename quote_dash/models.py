from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def regValidator(self, postData):
        errors = {}
        #input validations
        if len(postData['firstname']) < 2:
            errors['firstname'] = "First Name should atleast be 2 charecters"
        if len(postData['lastname']) < 2:
            errors['lastname'] = "Last Name should atleast be 2 charecters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        #check if entered email is unique
        if User.objects.filter(email=postData['email']):
            errors['email_unq'] = "This email is already registered!"
        if len(postData['password'] or postData['password_conf']) < 8:
            errors['password_len'] = "Password should atleast be 8 charecters"
        if postData['password'] != postData['password_conf']:
            errors['password_match'] = "Passwords do not match"
        return errors 

    def loginValidator(self, postData):
        errors = {}  
        #input validations not really needed as the email will be validated below anyway.
        # EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
        #     errors['email'] = "Invalid email address!"

        # if not (User.objects.filter(email=postData['email']) and User.objects.filter(password=postData['password'])):
        this_user = User.objects.filter(email=postData['email'])
        #check if the user exists (based on email)
        if (this_user):
            this_user = this_user[0]    #above 'filter' method returns a list of ONE object. So we reassign the var to the first element in the list.
            #compare hashed passwords
            if bcrypt.checkpw(postData['password'].encode(), this_user.password.encode()):
                print("LOGIN SUCCESSFUL")
                return errors
        else:
            errors['login'] = "Login failed! Check email and password"
        return errors 
    
    def updateValidator(self, postData, current_user_email):
        errors = {}
        #input validations
        if len(postData['firstname']) < 2:
            errors['firstname'] = "First Name should atleast be 2 charecters"
        if len(postData['lastname']) < 2:
            errors['lastname'] = "Last Name should atleast be 2 charecters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        #prevent the user from providing an email already registered with other user, but also allow to submit their same email again
        if postData['email'] != current_user_email:
            #now check if email is unique
            if User.objects.filter(email=postData['email']):
                errors['email_unq'] = "This email is already registered to another user!"
        return errors 


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def quoteValidator(self, postData):
        errors = {}
        #input validations
        if len(postData['author']) < 3:
            errors['author'] = "Author should atleast be 3 charecters"
        if len(postData['quote']) < 3:
            errors['quote'] = "Quote should atleast be 10 charecters"
        return errors 


class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="quotes", on_delete=models.CASCADE) #one to many
    liked_by = models.ManyToManyField(User, related_name="likes")  #many to many
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

# class Like(models.Model):
#     liked_by = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
#     liked_quote = models.

# class Comment(models.Model):
#     comment = models.TextField()
#     poster = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
#     on_message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
