from django.contrib import admin

from .models import User, Car, Comment, WatchList, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Car)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(Bid)