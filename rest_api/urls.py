from django.conf.urls import url, include
from rest_api import views

urlpatterns = [
    url(r'^login/$', views.Slogin, name='Login'),
    url(r'^logout/$', views.Slogout, name='Logout'),
    url(r'^register/$', views.register, name='Register'),
    url(r'^interests/$', views.interests, name='Interests'),
    url(r'^updatepref/$', views.updatepref, name='UpdatePreferences'),
    url(r'^getuserdata/$', views.getuserdata, name='GetUserData'),
    url(r'^synclocation/$', views.synclocation, name='SyncLocation'),
    url(r'^getmatches/(?P<sport_id>[0-9]+)', views.getmatches, name='GetMatches'),
]
