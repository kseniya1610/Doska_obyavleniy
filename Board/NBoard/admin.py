from lib2to3.pytree import Base
from django.contrib import admin
from .models import BoardNotice, Response

admin.site.register(BoardNotice)
admin.site.register(Response)
