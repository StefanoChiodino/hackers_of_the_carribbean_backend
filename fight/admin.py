from django.contrib import admin

# Register your models here.
from fight.models import Fight, Insult, Comeback, Step

admin.site.register(Fight)
admin.site.register(Insult)
admin.site.register(Comeback)
admin.site.register(Step)
