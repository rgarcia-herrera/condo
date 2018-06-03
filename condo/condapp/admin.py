from django.contrib import admin
from .models import Profile, Fee, Unit, \
    ProjectAttachment, Project, Quotation, Volunteer, Payment, \
    UnitType


class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 1


class FeeInline(admin.TabularInline):
    model = Fee
    extra = 1


class UnitAdmin(admin.ModelAdmin):
    inlines = [ProfileInline,
               FeeInline, ]

    list_filter = ('unit_type', )
    list_display = ['number', 'unit_type']


admin.site.register(Unit, UnitAdmin)
admin.site.register(Profile)
admin.site.register(UnitType)


class AttachmentInline(admin.TabularInline):
    model = ProjectAttachment
    extra = 1


class QuotationInline(admin.TabularInline):
    model = Quotation
    extra = 1


class VolunteerInline(admin.TabularInline):
    model = Volunteer
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'budget', 'creation_date',
                    'due_date', 'delivered']

    list_filter = ('due_date', 'delivered')

    inlines = [VolunteerInline,
               QuotationInline,
               AttachmentInline, ]


admin.site.register(Project, ProjectAdmin)


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1


class FeeAdmin(admin.ModelAdmin):
    inlines = [PaymentInline, ]

    list_display = ['name', 'ammount', 'unit', 'due_date', 'get_status']
    list_filter = ('due_date', 'unit')


admin.site.register(Fee, FeeAdmin)
