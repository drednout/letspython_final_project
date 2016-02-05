from django import forms
import redis
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from admintool.models import Players


class PlayerSearchForm(forms.Form):
    email = forms.CharField(label='E-mail', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Enter e-mail address here'}))


class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Login"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ChangeExpForm(ModelForm):
    class Meta:
        model = Players
        fields = [
            'xp',
        ]
        widgets = {
            'xp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter value here'}),
        }

    def clean_xp(self):
        value = self.cleaned_data.get('xp')
        value += self.instance.xp
        return value

    def save(self, commit=True):
        obj = super(ChangeExpForm, self).save(commit=False)
        redis_con = redis.StrictRedis(host='localhost', port=6379, db=0)
        redis_con.zadd('scores', obj.xp, obj.id)
        if commit:
            obj.save()
        return obj

