from django.contrib import admin
from .models import *

admin.site.register(Tariff)
admin.site.register(TariffCategory)
admin.site.register(Feedback)
# admin.site.register(Static)
admin.site.register(EmailSubscribe)
admin.site.register(Callback)
admin.site.register(Teacher)