from django.db import models

# Create your models here.
'''
class Hello(models.Model):
    name = models.CharField(max_length=45, null=True)
'''
class Simulation(models.Model):
    sid = models.IntegerField(primary_key=True) 
    dctcp = models.BooleanField(default=False)
    qfc = models.IntegerField()
    sfc = models.IntegerField()
    lfc = models.IntegerField()
    afc = models.IntegerField()
    done = models.BooleanField(default=False)

class Flow(models.Model):
    fid = models.IntegerField(primary_key=True) 
    ftype = models.CharField(max_length=1, null=True)
    start = models.IntegerField() #us
    end = models.IntegerField() #us
    deadline = models.IntegerField() #us
    src = models.CharField(max_length=5, )
    dst = models.CharField(max_length=5, )
    size = models.IntegerField()
    drcnt = models.IntegerField(default=0)
    thrput = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

    def __unicode__(self):
        flow_type = {'q':'query', 's':'short', 'l':'large'}
        return '<span>%s flow %d from [%s] to [%s], duration time is: %d us, dropped %d packet(s), flow size is %d and transferred %d Bytes</span><hr />' % (flow_type[self.ftype], self.fid, self.src, self.dst, self.end - self.start, self.drcnt, self.size, self.thrput)
