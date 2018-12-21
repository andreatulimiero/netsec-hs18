from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout

from .forms import *
from .models import *

PASS_COST = 10
DISALLOWED_SQL = ['select', 'insert', 'delete', 'create', 'update']

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
            account = Account.objects.create(user=user, balance=10, clear_password=raw_password)
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
            from_user = req.POST.get('from_user')
            from_user_pwd = req.POST.get('from_user_pwd')
            to_user_account = form.cleaned_data.get('to_user')
            amount = form.cleaned_data.get('amount')
            try:
                amount = int(amount)
                if amount < 0:
                    return HttpResponse('Te piacerebbe...', status=400)
            except Exception as e:
                return HttpResponse('Wrong amount',status=400)

            cursor = connection.cursor()
            row = cursor.execute("select user_id from passes_account where user_id = (select id from auth_user where username = '{}') and clear_password = '{}'".format(from_user, from_user_pwd))
            account_id = row.fetchone()
            print(account_id)

            if account_id is None:
                return HttpResponse('Oh no ...', status=401)
            sender = User.objects.filter(username=from_user).first()
            account_to = Account.objects.filter(id=int(to_user_account)).first()
            if account_to is None:
                return HttpResponse('No such account', status=400)

            account_from = Account.objects.filter(user=sender).first()
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
        if account.balance >= PASS_COST:
            account.balance -= PASS_COST
            account.save()
            success = True
        return render(req, 'passes/pass_reveal.html', {'success': success})

class GetAccountId(View):

    def get(self, req):
        if not req.user.is_authenticated:
            return redirect('index')
        form = SearchAccountForm()
        res = ''
        return render(req, 'passes/get_user_account.html', {'form':form, 'res': res})

    def post(self, req):
        if not req.user.is_authenticated:
            return redirect('index')

        form = SearchAccountForm()
        username = req.POST.get('username')
        if username.lower() in DISALLOWED_SQL:
            res = 'You cannot modify the DB'
        cursor = connection.cursor()
        accounts = cursor.execute("select id from passes_account where user_id = (select id from auth_user where username = '{}')".format(username))
        account_id = accounts.fetchone()
        if account_id is None:
            res = 'No account found'
        else:
            res = account_id
        return render(req, 'passes/get_user_account.html', {'form': form,'res': res})

