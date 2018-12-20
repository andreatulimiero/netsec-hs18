from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout

from .forms import *
from .models import *

PASS_COST = 10

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
            account = Account.objects.create(user=user, balance=10)
            return redirect('account')
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
                return redirect('account')
        return render(req, 'passes/login.html', {'form': form})

class Logout(View):

    def get(self, req):
        logout(req)
        return redirect('index')

class AccountView(View):

    def get(self, req):
        if not req.user.is_authenticated:
            return redirect('index')

        form = TransactionForm()
        balance = req.user.account.balance
        return render(req, 'passes/account.html', {'form': form, 'balance': balance})

    def post(self, req):
        if not req.user.is_authenticated:
            return redirect('index')

        form = TransactionForm(req.POST)
        if form.is_valid():
            from_user = form.cleaned_data.get('from_user')
            from_user_pwd = form.cleaned_data.get('from_user_pwd')
            to_user = form.cleaned_data.get('to_user')
            amount = form.cleaned_data.get('amount')
            try:
                amount = int(amount)
                if amount < 0:
                    return HttpResponse('Te piacerebbe...', status=400)
            except Exception as e:
                return HttpResponse('Wrong amount',status=400)
            sender = authenticate(req, username=from_user, password=from_user_pwd)
            if sender is None:
                return HttpResponse('Oh no ...', status=401)
            receiver = User.objects.filter(username=to_user).first()
            if receiver is None:
                return HttpResponse('No such user', status=400)

            account_from = Account.objects.filter(user=sender).first()
            account_to = Account.objects.filter(user=receiver).first()
            account_from.balance -= amount
            account_to.balance += amount
            account_from.save()
            account_to.save()
        return redirect('account') 

class BuyPassView(View):

    def get(self, req):
        if not req.user.is_authenticated:
            return redirect('index')

        account = req.user.account
        success = False 
        if account.balance > PASS_COST:
            account.balance -= PASS_COST
            account.save()
            success = True
        return render('passes/pass_reveal.html', {'success': success})


