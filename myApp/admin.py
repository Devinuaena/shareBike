from django.contrib import admin

# Register your models here.

from .models import Bike
from .models import Costumer
from .models import Operator
from .models import Manager

admin.site.register(Bike)
admin.site.register(Costumer)
admin.site.register(Operator)
admin.site.register(Manager)