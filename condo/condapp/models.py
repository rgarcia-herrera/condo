from django.db import models
from django.contrib.auth.models import User

class Appartment:
    number = models.CharField(max_length=200)

class Profile:
    phone = models.CharField(max_length=200)
    appartment = models.OneToOneField(Appartment)
    owner = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
class Project:
    name = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User)        
    budget = models.DecimalField(decimal_places=2)
    creation_date = models.DateField(auto_now=True)
    due_date = models.DateField()
    delivered = models.BooleanField(default=False)

class ProjectAttachment:
    project = models.ForeignKey(Project)
    attachment = models.FileField()
    
class Quotation:
    provider = models.CharField(max_length=200)
    user = models.ForeignKey(User)        
    project = models.ForeignKey(Project)
    price = models.DecimalField(decimal_places=2)
    attachment = models.FileField()

class ProjectVote:
    user = models.ForeignKey(User)    
    project = models.ForeignKey(Project)
    vote = models.BooleanField()

class Volunteer:
    user = models.ForeignKey(User)    
    project = models.ForeignKey(Project)    


class Fee:
    ammount = models.DecimalField(decimal_places=2)
    appartment = models.ForeignKey(Appartment)
    due_date = models.DateField()

    def get_status(self):
        return "pendiente"


class Payment:
    fee = models.ForeignKey(Fee)    
    date = models.DateField(auto_now=True)
    ammount = models.DecimalField(decimal_places=2)

