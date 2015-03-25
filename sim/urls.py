from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sim.views.home', name='home'),
    url(r'^addsim$', 'sim.views.addsim', name='addsim'),
    url(r'^flow$', 'sim.views.flow', name='flow'),
    url(r'^plot$', 'sim.views.plot', name='plot'),
)
