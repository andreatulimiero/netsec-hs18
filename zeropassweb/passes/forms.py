from django import forms

class UsernamePasswordForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class PassForm(forms.Form):
    key = forms.CharField(label='Key')
    pwd = forms.CharField(label='Password', widget=forms.PasswordInput())

class PassRevealForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    key = forms.CharField(label='Key')
