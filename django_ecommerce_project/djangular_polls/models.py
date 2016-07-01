from django.db import models

# Create your models here.

class Poll(models.Model):
    title = models.CharField(max_length=225)
    time_field = models.DateTimeField(auto_now_add=True)

    def pool_items(self):
        return self.poolitem_set.all()

class PollItem(models.Model):
    poll = models.ForeignKey(Poll, related_name='items')
    name = models.CharField(max_length=40)
    text = models.CharField(max_length=225)
    vote = models.IntegerField(default=0)
    percenteg = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    class Meta:
        ordering=["-text"]
