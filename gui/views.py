from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponseRedirect, Http404, HttpResponse
from API import models
import paramiko
import time
from datetime import datetime
# Create your views here.
def SingIn(request):
    if request.method == 'GET':
        context = ''
        return render(request, 'Page/SingIn.html', {'context': context})

    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/list')
        else:
            context = {'error': 'Wrong credintials'}  # to display error?
            return render(request, 'Page/SingIn.html', {'context': context})
def List(request,id=None):
    machins=models.Machin.objects.filter(user=request.user,user_monitor_permision=True)|models.Machin.objects.filter(other_monitor_permision=True)|models.Machin.objects.filter(group__in= models.Group.objects.filter(users=request.user),group_monitor_permision=True)
    machins=machins.order_by('id') 
    if not request.user.is_authenticated: raise Http404
    if request.method == 'GET': 
        return List_render(request,machins)
    elif request.method == 'POST':
        if 'id' in request.POST and id==0: models.Machin.objects.get(id=request.POST['id']).delete()
        elif 'group_filter' in request.POST:       
            machins=models.Machin.objects.all().filter(machin_group__id=request.POST['group_filter'])
            return List_render(request,machins)
        elif id!=None and id!=0:
            machin=models.Machin.objects.get(id=request.POST['id'])
            machin.name=request.POST['name']
            machin.group=models.Group.objects.get(id=request.POST['group'])
            machin.ip=request.POST['ip']
            machin.port=request.POST['port']
            machin.username=request.POST['username']
            if request.POST['password'] != "": machin.password=request.POST['password']
            machin.save()
        elif id==0: 
            machin=models.Machin()
            machin.name=request.POST['name']
            machin.group=models.Group.objects.get(id=request.POST['group'])
            machin.ip=request.POST['ip']
            machin.port=request.POST['port']
            machin.username=request.POST['username']
            machin.password=request.POST['password']
            machin.user=request.user
            machin.history_save=bool(request.POST['history_save'])
            machin.history_save=bool(request.POST['history_save'])
            machin.save() 
        return List_render(request,machins)
def List_render(request,machins):
    return render(request, 'Page/MachinList.html', {
        "machins": machins,
        "form":models.MachinForm(),
        "machin_groups":models.Machin_Group.objects.all()
        })
def connect_ssh(request,id):
    if not request.user.is_authenticated: raise Http404
    cmdout=""
    usr=request.user
    if request.method == 'POST':
        try:
            cmdout=ssh(id,usr,request.POST['cmdin'])
            print(cmdout)
        except:
            cmdout="ERROR connect"
    elif request.method == 'GET':
        try:
            cmdout=ssh(id,usr,"echo \"l_admin connect\"")
        except:
            cmdout="ERROR connect"
    return render(request, 'Page/Connect.html',{'cmdout':cmdout})
#no render
def ssh(id,usr,cmd):
    machin=models.Machin.objects.get(id=id)
    ssh_ = paramiko.SSHClient()
    ssh_.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_.connect(str(machin.ip.ip), port=machin.port, username=machin.username,password=machin.password, timeout=3)
    (stdin, stdout, stderr) = ssh_.exec_command(cmd)
    cmdout=stdout.read().decode("utf-8")
    ssh_.close()
    #log
    fph=f"media/machin/{machin.id}_{machin.name}.txt"
    fpl=f"media/log/{machin.id}_{machin.name}.txt"
    try:
        log=models.Log.objects.get(machin=machin)
    except:
        log=models.Log()
        log.machin=machin
        log.history.name=fph
        log.log.name=fpl
        log.save()
    if machin.history_save: 
        f = open(fph, "a")
        f.write("["+datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")+"] "+cmd+"\n")
        f.close()
    if machin.log_save: 
        f = open(fpl, "a")
        f.write(f"[{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}]connect {usr} to {str(machin.ip.ip)}:{machin.port}\n")
        f.close()
    print(log)
    return cmdout
def Logout(request):
    logout(request)
    return redirect('url-singin')
#StatusCustom
def handler400(request,exception): 
    response = render(request, "Page/Status.html", {"status": 400})
    response.status_code = 400
    return response
def handler403(request,exception):
    response = render(request, "Page/Status.html", {"status": 403})
    response.status_code = 403
    return response
def handler404(request,exception):  
    response = render(request, "Page/Status.html", {"status": 404})
    response.status_code = 404
    return response
def handler500(request):
    response = render(request, "Page/Status.html", {"status": 500})
    response.status_code = 500
    return response
