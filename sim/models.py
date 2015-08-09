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
    sc = models.IntegerField(default=0) #count of server 
    qf_thrput = models.IntegerField(default=0)
    lf_thrput = models.IntegerField(default=0)
    status = models.IntegerField(default=False)
    time = models.IntegerField(default=0)

    flow_list = None
    qrecord_list = None
    cwnd_list = None

    def __unicode__(self,):
        STATUS = ['UDONE', 'SIMING', 'DONE']
        return '[simulation %03d[%s,snd:%s,lfc:%s] %s query, %d short, and %d large,total:  %d flow, and it\' simulation is %s]' % (self.sid, self.tcptype, self.sc - 1, self.lfc, self.qfc, self.sfc, self.lfc, self.afc, STATUS[self.status])

    def query_flow_set(self,):
        return self.flow_set.filter(ftype='q')

    def short_flow_set(self,):
        return self.flow_set.filter(ftype='s')

    def large_flow_set(self,):
        return self.flow_set.filter(ftype='l')

class Flow(models.Model):
    fid = models.AutoField(primary_key=True) 
    ftype = models.CharField(max_length=1, null=True)
    start = models.IntegerField() #us
    end = models.IntegerField() #us
    deadline = models.IntegerField() #us
    src = models.CharField(max_length=5, )
    dst = models.CharField(max_length=5, )
    size = models.IntegerField(default=0)
    pktcnt = models.IntegerField(default=0)
    drcnt = models.IntegerField(default=0)
    thrput = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    sim = models.ForeignKey(Simulation)

    def __unicode__(self):
        flow_type = {'q':'query', 's':'short', 'l':'large'}
        FINISH = ['unfinished', 'finished']
        duraction = (self.end - self.start)
        if duraction < 1000:
            duraction = '%s us' % (duraction)
        elif duraction < 1000000:
            duraction = '%s ms' % (duraction/1000.0)
        else:
            duraction = '%s sec' % (duraction/1000000.0)

        r = '<span>%s flow %04d belongs to simulation %s, from [%s] to [%s], \
            duration time is: (%s->%s):%s, dropped %d packet(s), \
            flow size is %d and transferred %d Bytes(%d packets), is %s</span><hr />' \
            % (flow_type[self.ftype], self.fid, self.sim.sid, self.src, self.dst, \
            self.start/1000.0 , self.end/1000.0, duraction, \
            self.drcnt, self.size, self.thrput, self.pktcnt, FINISH[self.finished])
        return r

class Qrecord(models.Model):
    qid = models.AutoField(primary_key=True) 
    time = models.IntegerField(default=0)
    rack = models.IntegerField(default=0)
    server = models.IntegerField(default=0)
    pktcnt = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    sim = models.ForeignKey(Simulation)

    def __unicode__(self,):
        return 'Qrecord %s' % (self.qid)

class Cwnd(models.Model):
    cid = models.AutoField(primary_key=True) 
    time = models.IntegerField(default=0)
    qf = models.FloatField(default=0)
    sf = models.FloatField(default=0)
    lf = models.FloatField(default=0)
    sim = models.ForeignKey(Simulation)

    def __unicode__(self,):
        return 'Cwnd %s' % (self.cid)

    #def __unicode__(self,):
