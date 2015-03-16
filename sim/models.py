from django.db import models

# Create your models here.
'''
class Hello(models.Model):
    name = models.CharField(max_length=45, null=True)
'''
class Simulation(models.Model):
    sid = models.IntegerField(primary_key=True) 
    dctcp = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

class Flow(models.Model):
    fid = models.IntegerField(primary_key=True) 
    ftype = models.CharField(max_length=1, null=True)
    start = models.DecimalField(max_digits=8, decimal_places=6)
    end = models.DecimalField(max_digits=8, decimal_places=6)
    deadline = models.DecimalField(max_digits=8, decimal_places=6)
    src = models.IntegerField()
    dst = models.IntegerField()
    size = models.IntegerField()
    drcnt = models.IntegerField(default=0)
    thrput = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

    def __unicode__(self):
        return '<span>%d|%s|%f->%f|drcnt=%d|thrput=%d</span><hr />' % (self.fid, self.ftype, self.start, self.end, self.drcnt, self.thrput)
