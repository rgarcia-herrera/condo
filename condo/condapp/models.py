from django.db import models
from django.contrib.auth.models import User

class AptType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return "tipo: " + self.name
    
class Apartment(models.Model):
    number = models.CharField(max_length=200)
    apt_type = models.ForeignKey(AptType, on_delete=models.CASCADE)
    def __str__(self):
        return "depto %s, (%s)" % (self.number, self.apt_type)

class Profile(models.Model):
    phone = models.CharField(max_length=200)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    owner = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return "%s - %s" % (self.user, self.apartment)

    
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=19, decimal_places=2)
    creation_date = models.DateField(auto_now=True)
    due_date = models.DateField()
    delivered = models.BooleanField(default=False)

class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    attachment = models.FileField()
    
class Quotation(models.Model):
    provider = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    attachment = models.FileField(null=True, blank=True)

class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Fee(models.Model):
    ammount = models.DecimalField(max_digits=19, decimal_places=2)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    due_date = models.DateField()

    def get_status(self):
        return "pendiente"


class Payment(models.Model):
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    ammount = models.DecimalField(max_digits=19, decimal_places=2)

