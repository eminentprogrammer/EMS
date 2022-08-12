from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Student, Parent
from django.contrib.auth.models import Group


class AccountAdmin(UserAdmin):
    list_display = ('email','username','lastname','firstname','phone_number','account_type','date_joined', 'last_login', 'is_admin','is_student')
    search_fields = ('email','username',)
    readonly_fields=('date_joined', 'last_login')
    
    ordering = ["username"]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)


admin.site.register(Student)

admin.site.register(Parent)

admin.site.unregister(Group)

