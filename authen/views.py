from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def register_user(request):
    context = {}
    msg = ''
    if request.method == "POST":

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        username = request.POST.get("username")
        email = request.POST.get("email")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")

        if password1 == password2 and len(password1)>4 and not User.objects.filter(username=username):
            msg = 'Success!'
            user = User.objects.create_user(
                username=username, 
                email=email,
                password=password1,
                first_name=fname,
                last_name=lname)
        else:
            msg = "Password doesn't math and Password must be than 4 character or Username's already used."
            context['username'] = username
            context['password1'] = password1
            context['password2'] = password2
            context['fname'] = fname
            context['lname'] = lname
            context['email'] = email
            
    context['msg'] = msg

    return render(request, 'authen/register.html', context=context)

def login_user(request):
    context = {}
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user:
            login(request, user)
            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            context['error'] = 'Username or Password wrong!'
            context['username'] = username
            context['password'] = password
    next_url = request.GET.get("next")
    if next_url:
        context['next_url'] = next_url

    return render(request, 'authen/login.html', context=context)

def logout_user(request):
    logout(request)
    return redirect('login_user')














