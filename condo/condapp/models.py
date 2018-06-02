from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class AptType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return "tipo: " + self.name

    class Meta:
        verbose_name = _('Apartment type')
        verbose_name_plural = _('Apartment types')


class Apartment(models.Model):
    number = models.CharField(_('number'),
                              max_length=200,
                              help_text=_('Apartment number'))
    apt_type = models.ForeignKey(AptType,
                                 help_text=_('Type of apartment'),
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Apartment')
        verbose_name_plural = _('Apartments')

    def __str__(self):
        return _("apartment") + "%s, (%s)" % (self.number, self.apt_type)


class Profile(models.Model):
    phone = models.CharField(_('phone number'),
                             max_length=200)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    owner = models.BooleanField(_('owner'))
    user = models.OneToOneField(User,
                                verbose_name=_('user'),
                                on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.user, self.apartment)


class Project(models.Model):
    name = models.CharField(_('name'),
                            max_length=200)
    description = models.TextField(_('description'))
    user = models.ForeignKey(User,
                             verbose_name=_('author'),
                             on_delete=models.CASCADE)
    budget = models.DecimalField(_('budget'),
                                 max_digits=19,
                                 decimal_places=2)
    creation_date = models.DateField(_('creation date'),
                                     auto_now=True)
    due_date = models.DateField(_('due date'),)
    delivered = models.BooleanField(_('delivered'),
                                    default=False)

    def __str__(self):
        delivered = _("delivered") if self.delivered else ""
        return "%s $%02f %s %s" % (self.name, self.budget,
                                   self.due_date, delivered)


class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    attachment = models.FileField()
    date = models.DateField(auto_now=True)


class Quotation(models.Model):
    provider = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    attachment = models.FileField(null=True, blank=True)
    date = models.DateField(auto_now=True)


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Fee(models.Model):
    name = models.CharField(max_length=200)
    ammount = models.DecimalField(max_digits=19, decimal_places=2)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    due_date = models.DateField()

    def get_status(self):
        return "pendiente"

    def __str__(self):
        return "%s %s %s %s" % (self.name, self.ammount,
                                self.apartment, self.due_date)


class Payment(models.Model):
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    ammount = models.DecimalField(max_digits=19, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s %s" % (self.date, self.fee, self.ammount, self.user)
