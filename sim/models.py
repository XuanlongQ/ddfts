from django.db import models

# Create your models here.
'''
class Hello(models.Model):
    name = models.CharField(max_length=45, null=True)
'''
class Simulation(models.Model):
    sid = models.AutoField(primary_key=True) 
    tcptype = models.CharField(max_length=10, null=True)
    qfc = models.IntegerField(default=0)
    sfc = models.IntegerField(default=0)
    lfc = models.IntegerField(default=0)
    afc = models.IntegerField(default=0)
    status = models.IntegerField(default=False)
    time = models.IntegerField(default=0)

    def __unicode__(self,):
        STATUS = ['UDONE', 'SIMING', 'DONE']
        return '[simulation %03d[%s] has %s query flow, %d short flow, and %d large flow, which totally has %d flow, and it\' simulation is %s]' % (self.sid, self.tcptype, self.qfc, self.sfc, self.lfc, self.afc, STATUS[self.status])

class Flow(models.Model):
    fid = models.AutoField(primary_key=True) 
    ftype = models.CharField(max_length=1, null=True)
    start = models.IntegerField() #us
    end = models.IntegerField() #us
    deadline = models.IntegerField() #us
    src = models.CharField(max_length=5, )
    dst = models.CharField(max_length=5, )
    size = models.IntegerField()
    pktcnt = models.IntegerField(default=0)
    drcnt = models.IntegerField(default=0)
    thrput = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    sim = models.ForeignKey(Simulation)

    def __unicode__(self):
        flow_type = {'q':'query', 's':'short', 'l':'large'}
        FINISH = ['unfinished', 'finished']
        return '<span>%s flow %04d belongs to simulation %s, from [%s] to [%s], duration time is: (%s->%s):%s us, dropped %d packet(s), flow size is %d and transferred %d Bytes(%d packets), is %s</span><hr />' \
% (flow_type[self.ftype], self.fid, self.sim.sid, self.src, self.dst, \
self.start/1000.0 , self.end/1000.0, self.end - self.start, \
self.drcnt, self.size, self.thrput, self.pktcnt, FINISH[self.finished])

class Qrecord(models.Model):
    qid = models.AutoField(primary_key=True) 
    time = models.IntegerField(default=0)
    rack = models.IntegerField(default=0)
    server = models.IntegerField(default=0)
    pktcnt = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    sim = models.ForeignKey(Simulation)

    #def __unicode__(self,):
