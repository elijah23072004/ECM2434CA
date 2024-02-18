from django import forms
#from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm
from ecomap.models import User

#from django.contrib.auth.models import User

#class RegisterForm(UserCreationForm):
class RegisterForm(ModelForm):
    #firstname=forms.CharField(label="firstname",max_length=100, required=True)
    #lastname=forms.CharField(label="lastname",max_length=100, required=True)
    #username=forms.CharField(label="username",max_length=100, required=True)
    #password=forms.CharField(label="password",max_length=512, required=True)
    userType=forms.CharField(label="userType",max_length=20, required=False)
    
    

    class Meta:
        model = User
        fields = ["username","first_name","last_name","password","userType"]
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


