from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UnitType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Unit type')
        verbose_name_plural = _('Unit types')


class Unit(models.Model):
    number = models.CharField(_('number'),
                              max_length=200,
                              help_text=_('Room number'))
    unit_type = models.ForeignKey(UnitType,
                                  help_text=_('e.g. apartment, shop, etc.'),
                                  on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Apartment')
        verbose_name_plural = _('Apartments')

    def __str__(self):
        return "%s %s" % (self.apt_type, self.number)


class Profile(models.Model):
    phone = models.CharField(_('phone number'),
                             max_length=200)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    owner = models.BooleanField(_('owner'))
    user = models.OneToOneField(User,
                                verbose_name=_('user'),
                                on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.user, self.apartment)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


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

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    attachment = models.FileField()
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')


class Quotation(models.Model):
    provider = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    attachment = models.FileField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('Quotation')
        verbose_name_plural = _('Quotations')


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Voluntario')
        verbose_name_plural = _('Voluntarios')


class Fee(models.Model):
    name = models.CharField(max_length=200)
    ammount = models.DecimalField(max_digits=19, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    due_date = models.DateField()

    class Meta:
        verbose_name = _('Fee')
        verbose_name_plural = _('Fees')

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

    class Meta:
        verbose_name = _('Pago')
        verbose_name_plural = _('Pagos')
