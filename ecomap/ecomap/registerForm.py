from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm
from ecomap.models import User


class RegisterForm(ModelForm):
    """
    A form for registering a new user.

    Inherits from Django's ModelForm class and adds additional fields for userType, score, and streak.
    """

    # Define additional fields
    userType = forms.CharField(label="userType", max_length=20, required=False)  # Field for user type
    score = forms.IntegerField(label="score", required=False)  # Field for user score
    streak = forms.IntegerField(label="streak", required=False)  # Field for user streak
    last_played = forms.DateField(label="last_played", required=False)  #Field for when the user last played
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password", "userType", "score", "streak", "last_played"]
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


