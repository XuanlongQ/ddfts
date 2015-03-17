from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sim.views.home', name='home'),
    url(r'^flow$', 'sim.views.flow', name='flow'),
    url(r'^plot$', 'sim.views.plot', name='plot'),
)
