from django.contrib import admin

# Register your models here.
from .models import User, Series, Specialities, Subjects

admin.site.register(User)
admin.site.register(Series)
admin.site.register(Specialities)
admin.site.register(Subjects)