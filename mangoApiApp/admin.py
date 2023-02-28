from django.contrib import admin
from .models import BankAccount,Clients,PayInobject,CardWebPayInobject


class PayInobjectAdmin(admin.ModelAdmin):
    list_display=('ReturnURL','CardType','SecureMode','Billing','Culture','Shipping','TemplateURL','StatementDescriptor','RedirectURLstring')





# admin.site.register(PayInobject, PayInobjectAdmin)
# admin.site.register(User,UserAdmin)

# # Register your models here.
