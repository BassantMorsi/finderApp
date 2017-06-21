from django.contrib import admin
from .models import User
from .models import FindRequest
from .models import MissRequest

# Register your models here.

admin.site.register(User)
admin.site.register(FindRequest)
admin.site.register(MissRequest)



