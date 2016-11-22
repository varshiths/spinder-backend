import json
import urllib.request
import urllib.error

import math
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core import serializers
# from django.db.models import F
import django.shortcuts
from django.views.decorators.csrf import csrf_exempt

from rest_api.models import *


def details(user):
    det = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
           'playing_time': user.play_time, 'enthu_level': user.enthu_level, 'exp' : user.expertise_level,
           'interests': json.loads(serializers.serialize('json', user.interests.all()))}
    # print(det)
    # det = json.dumps(det, indent=2)
    return det


@csrf_exempt
def Slogin(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            userObject = SUser.objects.get(username=username)
            data = details(userObject)
            # print(data)
            return django.shortcuts.HttpResponse(json.dumps(data))
        else:
            return django.shortcuts.HttpResponse('{"success" : false}')
    else:
        return django.shortcuts.HttpResponse('{"success" : false}')


@login_required(login_url='/login/')
def Slogout(request):
    if request.method == 'GET':
        logout(request)
        return django.shortcuts.HttpResponse('{"success" : true}')
    else:
        print('Request Error')
        return django.shortcuts.HttpResponse('{"success" : false}')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        user = SUser()
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.set_password(request.POST['password'])
        user.save()
        return django.shortcuts.HttpResponse('{"success" : true}')
    else:
        print('Request Error')
        return django.shortcuts.HttpResponse('{"success" : false}')


@login_required(login_url='/login/')
def interests(request):
    if request.method == 'GET':
        user = request.user
        data = serializers.serialize('json', user.interests.all())
        return django.shortcuts.HttpResponse(data)
    else:
        print('Request Error')
        return django.shortcuts.HttpResponse('{"success" : false}')


@csrf_exempt
@login_required(login_url='/login/')
def updatepref(request):
    if request.method == 'POST':
        user = SUser.objects.get(pk = request.user.pk)
        for key in request.POST:
            if key == 'username':
                user.username = request.POST[key]
            if key == 'exp':
                user.expertise_level = request.POST[key]
            if key == 'first_name':
                user.first_name = request.POST[key]
            if key == 'last_name':
                user.last_name = request.POST[key]
            if key == 'interests':
                print(user.interests.all())

                for i in user.interests.all():
                    user.interests.remove(Sport.objects.get(pk = i.pk))

                print(user.interests.all())

                list = request.POST[key][1:].split(',')
                for pkcode in list:
                    user.interests.add(Sport.objects.get(pk = pkcode))

                print(user.interests.all())
        return django.shortcuts.HttpResponse('{"success" : true }')
    else:
        data = serializers.serialize('json', Sport.objects.all())
        return django.shortcuts.HttpResponse(data)


@csrf_exempt
@login_required(login_url='/login/')
def synclocation(request):
    if request.method == 'POST':
        user = SUser.objects.get(pk=request.user.pk)
        user.lat = float(request.POST['lat'])
        print(user.lat)
        user.long = float(request.POST['long'])
        print(user.long)
        user.save()
        print("location synced")
        return django.shortcuts.HttpResponse('{"success" : true}')
    else:
        print('Request Error')
        return django.shortcuts.HttpResponse('{"success" : false}')


def pathdistance(lat1, long1, lat2, long2):
    bing_key = 'key=' + 'MwO7OwpAWovkMKPdoBxI~K7XSLiSgXeAkpB8zxJn-8A~AuvqAwSn_Jh1Imf62IFh3g2LPfTRl11y33PK2dyaQxcHJChrewr98-IXBdm0pBt8'
    url = 'http://dev.virtualearth.net/REST/v1/Routes?'
    start = 'wayPoint.1=' + str(lat1) + ',' + str(long1) + '&'
    end = 'wayPoint.2=' + str(lat2) + ',' + str(long2) + '&'
    optimize = 'optimize=' + 'distance' + '&'
    requrl = url + start + end + optimize + bing_key
    # print(requrl)
    try:
        resp = urllib.request.urlopen(requrl)
        data = resp.read().decode('utf-8')
        data = json.loads(str(data))
        data = data['resourceSets'][0]['resources'][0]['travelDistance']
    except Exception:
        data = math.pow(2, 31) - 1
    # print(data)
    return int(data)



def trtrtr(x,user):
    try:
        return abs(x.score - user.score) * exp(pathdistance(user.lat, user.long, x.lat, x.long) / 5)
    except Exception:
        return pow(2, 31)-1


def matchevaluate(user, sport_id):
    list = Sport.objects.get(pk=sport_id).suser_set.all()
    # print(list)
    # print(sport_id)
    list = sorted(list, key=lambda x: trtrtr(x, user))
    details_list = []
    for item in list:
        details_list.append(details(item))
    return details_list[1:5]


@login_required(login_url='/login/')
def getuserdata(request):
    return django.shortcuts.HttpResponse(json.dumps(details(SUser.objects.get(username=request.user.username))))


@login_required(login_url='/login/')
def getmatches(request, sport_id):
    if request.method == 'GET':
        user = SUser.objects.get(username=request.user.username)
        matchedusers = matchevaluate(user, sport_id)
        return django.shortcuts.HttpResponse(str(matchedusers))
    else:
        print('Request Error')
        return django.shortcuts.HttpResponse('{"success" : false}')
