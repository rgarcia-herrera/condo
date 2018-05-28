from django.contrib import admin

from .models import *

admin.site.register(AptType)

class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 1

class FeeInline(admin.TabularInline):
    model = Fee
    extra = 1
    
class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ProfileInline,
               FeeInline, ]
    list_filter = ('apt_type', )

    list_display = ['number', 'apt_type' ]

    
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(ProjectAttachment)
admin.site.register(Quotation)
admin.site.register(Volunteer)
admin.site.register(Fee)
admin.site.register(Payment)
