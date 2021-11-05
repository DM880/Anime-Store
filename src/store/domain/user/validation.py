from django.contrib.auth import authenticate, login, logout


from store.data.user.models import CustomUser as User


def sign_up_validation(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if User.objects.filter(username=username).exists():
        return "{} - Username already exist".format(username)

    elif User.objects.filter(email=email).exists():
        return "{} - Email already exist".format(email)

    elif password1 != password2:
        return "Passwords don't match"

    else:
        data_user = {
            'first_name':request.POST.get('fname'),
            'last_name':request.POST.get('lname'),
            'username':request.POST.get('username'),
            'date_of_birth':request.POST.get('birth'),
            'email':request.POST.get('email'),
            'password':request.POST.get('password1'),
            }

        User.objects.create_user(**data_user)
        return True


def sign_in_validation(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(email=email, password=password)

    if user:
        if user.is_active:
            login(request, user)
            return True
    return False
