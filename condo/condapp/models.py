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
        return "%s %s" % (self.unit_type, self.number)


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


class RecurrentFee(models.Model):
    name = models.CharField(max_length=200)
    ammount = models.DecimalField(max_digits=19, decimal_places=2)
    unit_type = models.ForeignKey(UnitType,
                                  help_text=_('unit type to apply recurrent fee'),
                                  on_delete=models.CASCADE)
    weekdays = models.CharField(max_length=200)
    monthdays = models.CharField(max_length=200)
    months = models.CharField(max_length=200)

    class Meta:
        verbose_name = _('Fee')
        verbose_name_plural = _('Fees')

    def get_status(self):
        return "pendiente"

    def __str__(self):
        return "%s %s %s %s" % (self.name, self.ammount,
                                self.apartment, self.due_date)


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


class Deposit(models.Model):
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    ammount = models.DecimalField(max_digits=19, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s %s" % (self.date, self.fee, self.ammount, self.user)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')


class Withdrawal(models.Model):
    date = models.DateField(auto_now=True)
    ammount = models.DecimalField(max_digits=19, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attachment = models.FileField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class RotatingPosition(models.Model):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'))
    weekdays = models.CharField(max_length=200)
    monthdays = models.CharField(max_length=200)
    months = models.CharField(max_length=200)
    units = models.ManyToManyField(Unit)

    def create_position(self):
        """
        If now() matches monthdays, weekdays and months
        create entry in Position table with name and description.
        
        User is selected among profiles associated to units, by
        rotation. Uses rotation_id to tell who goes next.
        """
        pass


class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=200)
    description = models.TextField(_('description'))
    rotation = models.ForeignKey(RotatingPosition, null=True, blank=True)
    


class Announcements(models.Model):
    user = models.ForeignKey(User, default=creator, null=True)
    date = models.DateField(auto_now=True)
    title = models.CharField(max_length=200)
    text = models.TextField(_('description'))

    def creator(self):
        """
        try to get user from session?
        or None if an auto-created announcement
        """
    
