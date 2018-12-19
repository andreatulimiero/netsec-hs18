from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout

from .forms import UsernamePasswordForm, PassForm, PassRevealForm
from .models import Pass

# Create your views here.
class Index(View):

    def get(self, req):
        return render(req, 'passes/index.html')

class Signup(View):

    def get(self, req):
        form = UserCreationForm()
        return render(req, 'passes/signup.html', {'form': form})
    
    def post(self, req):
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(req, user)
            return redirect('passes')
        else:
            return render(req, 'passes/signup.html', {'form': form})

class Login(View):

    def get(self, req):
        form = UsernamePasswordForm()
        return render(req, 'passes/login.html', {'form': form})

    def post(self, req):
        form = UsernamePasswordForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('passes')
        return render(req, 'passes/login.html', {'form': form})

class Logout(View):

    def get(self, req):
        logout(req)
        return redirect('index')

class PassCRUD(View):

    def get(self, req):
        if not req.user.is_authenticated:
            return redirect('index')

        form = PassForm()
        passes = Pass.objects.filter(user=req.user).all()
        return render(req, 'passes/passes.html', {'passes': passes, 'form': form})

    def post(self, req):
        if not req.user.is_authenticated:
            return redirect('index')

        passes = Pass.objects.filter(user=req.user).all()
        form = PassForm(req.POST)
        if form.is_valid():
            key = form.cleaned_data.get('key')
            pwd = form.cleaned_data.get('pwd')
            user = req.user
            p = Pass.objects.create(user=user, key=key, pwd=pwd)
            p.save()
            return redirect('passes') 
        return render(req, 'passes/passes.html', {'passes': passes, 'form': form})

class PassReveal(View):

    def get(self, req, key):
        if not req.user.is_authenticated:
            return redirect('index')

        form = UsernamePasswordForm()
        passes = Pass.objects.filter(user=req.user).all()
        return render(req, 'passes/pass_reveal.html', {'form': form})

    def post(self, req, key):
        form = UsernamePasswordForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(req, username=username, password=password)
            if user is None:
                return HttpResponse('te piacerebbe', status=401)

            pss = Pass.objects.filter(user=user, key=key).first()
            if pss is None:
                return HttpResponse(status=404) 
            print(pss)

            return render(req, 'passes/pass_reveal.html', {'pass': pss, 'form': form})
        return render(req, 'passes/pass_reveal.html', {'form': form})
        

