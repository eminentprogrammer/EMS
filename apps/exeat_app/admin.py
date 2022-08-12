from django.contrib import admin
from .models import Exeat

class ExeatAdmin(admin.ModelAdmin):
    list_display = ('student', 'reason', 'leave_on','return_on')

admin.site.register(Exeat, ExeatAdmin)