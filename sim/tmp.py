import commands, time

while True:
    status, output = commands.getstatusoutput('mysql -uroot -p123 -e"select count(*) from ddfts.sim_qrecord;"')
    print '++++++++++++++qrecord =', output.split('\n')[1] 
    time.sleep(1)
