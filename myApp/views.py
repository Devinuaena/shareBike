from django.shortcuts import render,HttpResponse,redirect
from .models import Bike
from .models import Costumer
from .models import Operator
from .models import Manager
import json
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from django.http import HttpResponse
def index(request):
    return render(request, 'myApp/index.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'myApp/login.html')
    if request.method == 'POST':
        uname = request.POST.get('username')
        upwd = request.POST.get('userPassword')
        ubalance = Costumer.costumerObj.all().values('balance').get(username=uname)
        ubal = ubalance.get('balance')
        if uname == '':
            return JsonResponse({'success': '203', 'msg': 'Username can not be empty!'})
        else:
            if upwd == '':
                return JsonResponse({'success': '204', 'msg': 'Password can not be empty!'})
            else:
                user_obj = Costumer.costumerObj.filter(username=uname).first()
                if user_obj:
                    pass_obj = Costumer.costumerObj.filter(userpassword=upwd).first()
                    if pass_obj:
                        return JsonResponse({'success': '200', 'msg': 'Success', 'username': uname, 'balance': ubal})
                    else:
                        return JsonResponse({'success': '202', 'msg': 'Entered wrong passwords!'})
                else:
                    return JsonResponse({'success': '201', 'msg': 'Username not existed!'})


def register(request):
    if request.method == 'GET':
        return render(request, 'myApp/register.html')
    if request.method == 'POST':
        uname = request.POST.get('username')
        upwd = request.POST.get('userPassword')
        re_upwd = request.POST.get('userRePassword')
        utel = request.POST.get('usertelephone')
        if uname and upwd and re_upwd:
            if upwd == re_upwd:
                user_obj = Costumer.costumerObj.filter(username=uname).first()
                if user_obj:
                    return  JsonResponse({'success': '201', 'msg': 'Username existed!'})
                else:
                    Costumer.costumerObj.create(username=uname, userpassword=upwd, telephone=utel,balance=0).save()
                    return JsonResponse({'success': '200', 'msg': 'Register successfully!'})
            else:
                return  JsonResponse({'success': '202', 'msg': 'Entered passwords differ!'})

        else:
            return  JsonResponse({'success': '203', 'msg': 'Can not be empty!'})

def user(request):
    uname = request.GET.get('username')
    ubal = request.GET.get('balance')
    selectbikeid = request.GET.get('selectbikeid')
    renttime = request.GET.get('renttime')
    cost = request.GET.get('cost')
    return render(request, 'myApp/user.html',{'username':uname, 'balance':ubal, 'selectbikeid':selectbikeid,'renttime':renttime,'cost':cost})

def customer(request):
    if request.method == 'GET':
        return render(request, 'myApp/login.html')
    if request.method == 'POST':
        uname = request.POST.get('username')
        ubal = request.POST.get('balance')
        top = request.POST.get('topup')
        topup = float(top)
        uTop = Costumer.costumerObj.all().values('balance').get(username=uname)
        utop = float(uTop.get('balance'))
        userTop = Costumer.costumerObj.filter(username=uname).update(balance=utop+topup)
        newTop = Costumer.costumerObj.all().values('balance').get(username=uname)
        newuTop = float(newTop.get('balance'))
        return JsonResponse({'success': '200', 'msg': 'Top up successfully!','username':uname,'balance':newuTop})

# def showbike(request):
#     if request.method == 'GET':
#         return render(request,'myApp/user.html')
#     if request.method == 'POST':
#         query_bike = list(Bike.bikeObj.objects.all().values('id','bikeid'))
#         print(query_bike)
#     return JsonResponse(query_bike)

def selectbike(request):
    if request.method == 'GET':
        return render(request,'myApp/user.html')
    if request.method == 'POST':
        uname = request.POST.get('username')
        ubal = request.POST.get('balance')
        selbike = request.POST.get('selectbike')
        used = Bike.bikeObj.values('isused').get(bikeid=selbike)
        rent = datetime.now()
        rentTime = rent.strftime('%Y-%m-%d %H:%M:%S')
        renttime = Costumer.costumerObj.filter(username=uname).update(renttime=rent)
        if used.get('isused') == False:
            isused = Bike.bikeObj.filter(bikeid=selbike).update(isused = '1')
            return JsonResponse({'success': '201', 'msg': 'Rent successfully!','username':uname,'balance':ubal,'selectbike':selbike,'renttime':rentTime})
        else:
            return JsonResponse({'success': '202', 'msg': 'Rent failly!','username':uname,'balance':ubal})

def brokenbike(request):
    if request.method == 'GET':
        return render(request,'myApp/user.html')
    if request.method == 'POST':
        uname = request.POST.get('username')
        ubal = request.POST.get('balance')
        selbike = request.POST.get('brokenbike')
        stat = Bike.bikeObj.filter(bikeid=selbike).update(statement = '0')
        if stat:
            return JsonResponse({'success': '203', 'msg': 'Notify successfully!','username':uname,'balance':ubal})
        else:
            return JsonResponse({'success': '204', 'msg': 'Notify failly!','username':uname,'balance':ubal})

def returnbike(request):
    if request.method == 'GET':
        return render(request,'myApp/user.html')
    if request.method == 'POST':
        uname = request.POST.get('username')
        ubal = request.POST.get('balance')
        selectbike = request.POST.get('selectbikeid')
        rent = request.POST.get('renttime')
        rentTime = datetime.strptime(rent, '%Y-%m-%d %H:%M:%S')
        selbike = request.POST.get('returnbike')
        used = Bike.bikeObj.values('isused').get(bikeid=selbike)
        retime = datetime.now()
        returntime = Costumer.costumerObj.filter(username=uname).update(returntime=retime)
        charTime = (retime - rentTime).seconds
        print(charTime)
        if charTime <= 30*60:
            cost = 1
            print(cost)
        elif charTime <= 60*60 and charTime > 30*60:
            cost = 2
        else:
            cost = 10
        if used.get('isused') == True:
            isused = Bike.bikeObj.filter(bikeid=selbike).update(isused = '0')
            return JsonResponse({'success': '205', 'msg': 'Return successfully!', 'username': uname, 'balance': ubal, 'selectbikeid':'None','renttime':'None', 'cost':cost})
        else:
            return JsonResponse({'success': '206', 'msg': 'Return failly!', 'username': uname, 'balance': ubal})

def pay(request):
    if request.method == 'GET':
        return render(request, 'myApp/user.html')
    if request.method == 'POST':
        uname = request.POST.get('username')
        ubal = request.POST.get('balance')
        money = request.POST.get('cost')
        bbal = float(ubal) - float(money)
        less = Costumer.costumerObj.filter(username=uname).update(balance=bbal)
        if less:
            return JsonResponse({'success': '207', 'msg': 'Pay successfully!', 'username': uname, 'balance': bbal})
        else:
            return JsonResponse({'success': '208', 'msg': 'Pay failly!', 'username': uname, 'balance': bbal})

def userSetting(request):
    bid = request.GET.get('bbikeid')
    blocation = request.GET.get('bikelocation')
    bstat = request.GET.get('bikestatement')
    return render(request, 'myApp/userSetting.html',{'bbikeid': bid, 'bikelocation': blocation, 'bikestatement':bstat})

def trackbike(request):
    if request.method == 'GET':
        return render(request, 'myApp/userSetting.html')
    if request.method == 'POST':
        bid = request.POST.get('bikelocationid')
        blocation = Bike.bikeObj.values('bikelocation').get(bikeid=bid)
        bblo = blocation.get('bikelocation')
        bstat = Bike.bikeObj.values('statement').get(bikeid=bid)
        if bstat.get('statement') == True:
            return JsonResponse({'success': '209', 'msg': 'Track successfully, Available bike!', 'bbikeid': bid, 'bikelocation': bblo, 'bikestatement':'Well'})
        if bstat.get('statement') == False:
            return JsonResponse({'success': '210', 'msg': 'Track successfully, Broken bike!', 'bbikeid': bid, 'bikelocation': bblo, 'bikestatement': 'Broken'})
        if bstat.get('statement') == None:
            return JsonResponse({'success': '211', 'msg': 'Track failly!', 'bbikeid': bid, 'bikelocation': 'None','bikestatement': 'None'})


def fixbike(request):
    if request.method == 'GET':
        return render(request, 'myApp/userSetting.html')
    if request.method == 'POST':
        fid = request.POST.get('fixbikeid')
        blocation = Bike.bikeObj.values('bikelocation').get(bikeid=fid)
        bblo = blocation.get('bikelocation')
        bstat = Bike.bikeObj.filter(bikeid=fid).update(statement='1')
        if bstat:
            return JsonResponse({'success': '212', 'msg': 'Fix successfully!', 'bbikeid': fid, 'bikelocation': bblo,'bikestatement':'Well'})
        else:
            return JsonResponse({'success': '213', 'msg': 'Fix failly!', 'bbikeid': fid, 'bikelocation': blocation})

def changelocation(request):
    if request.method == 'GET':
        return render(request, 'myApp/userSetting.html')
    if request.method == 'POST':
        cid = request.POST.get('bbikeid')
        bstat = request.POST.get('bikestatement')
        clocation = request.POST.get('changelocation')
        cloc = Bike.bikeObj.filter(bikeid=cid).update(bikelocation=clocation)
        blocation = Bike.bikeObj.values('bikelocation').get(bikeid=cid)
        bblo = blocation.get('bikelocation')
        if cloc:
            return JsonResponse({'success': '212', 'msg': 'Change successfully!', 'bbikeid': cid, 'bikelocation': bblo,'bikestatement':bstat})
        else:
            return JsonResponse({'success': '213', 'msg': 'Change failly!', 'bbikeid': cid, 'bikelocation': bblo,'bikestatement':bstat})

def adminManager(request):
    return render(request, 'myApp/adminManager.html', {})