#from .models import User


#def loginAuth(username, password):
#    try:
#        user = User.objects.get(username=username)
#    except Exception as e:
#        return False, e

#    if password == user.password:
#        return True, "Valid Login"
#    else:
#        return False, "Invalid Password"

from django.shortcuts import render
from .models import User
from .utils import loginAuth

def login(request):
    if request.method == 'POST':
        username = request.POST.get('InputtedUsername')
        password = request.POST.get('InputtedPassword')
        authenticated, message = loginAuth(username, password)
        if authenticated:
            # If login is successful, redirect to the home page or any other desired page
            return redirect('home')
        else:
            # If login fails, reload the login page with an error message
            error_message = message
            return render(request, 'login.html', {'error_message': error_message})
    else:
        # If it's a GET request, render the login page
        return render(request, 'login.html')



