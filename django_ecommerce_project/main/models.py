from django.db import models
from datetime import datetime as dt
# Create your models here.

class Status(models.Model):
    user = models.ForeignKey('payments.User')
    status = models.CharField(max_length=225)
    time_added = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return 'Status({}, {}, {})'.format(self.user, self.status, self.time_added)
