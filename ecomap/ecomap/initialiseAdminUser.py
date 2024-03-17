import sys
from .models import User as EcomapUser
from django.contrib.auth.models import User


def initialiseAdminUser(username,first_name, last_name, password):
    admin = EcomapUser.objects.create(username=username, password=password, userType="admin",first_name=first_name, last_name=last_name)
    user = User.objects.create_user(username, password=password)
    user.save()
    print("user created ", username)


def main():
    initialiseAdminUser(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])

if __name__=="__main__":
    main()