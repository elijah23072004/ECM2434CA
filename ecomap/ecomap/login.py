from .models import User


def loginAuth(username, password):
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        return False, e

    if password == user.password:
        return True, "Valid Login"
    else:
        return False, "Invalid Password"


