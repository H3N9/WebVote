from django.contrib import admin
from django.contrib.auth.models import Permission

# Register your models here.

from poll.models import Poll, Poll_Choice, Poll_Vote

admin.site.register(Poll)
admin.site.register(Poll_Choice)
admin.site.register(Poll_Vote)
admin.site.register(Permission)
