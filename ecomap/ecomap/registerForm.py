from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm
from ecomap.models import User


class RegisterForm(ModelForm):
    userType=forms.CharField(label="userType",max_length=20, required=False)
    score=forms.IntegerField(label="score",required=False)
    streak=forms.IntegerField(label="streak",required=False)
    
    class Meta:
        model = User
        fields = ["username","first_name","last_name","password","userType","score","streak"]
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


