from django import forms

class UsernamePasswordForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class TransactionForm(forms.Form):
    from_user = forms.CharField(label='Sending user')
    from_user_pwd = forms.CharField(label='Password of sending user')
    to_user = forms.CharField(label='Receiving user')
    amount = forms.IntegerField(label='Amount of the transfer')

