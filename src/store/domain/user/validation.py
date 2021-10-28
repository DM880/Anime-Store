from store.data.user.models import CustomUser as User


# def username_validation(request):
#     username = request.POST.get('username')
#     if User.objects.filter(username=username).exists():
#         return True
#     else:
#         return False


# def password_validation(request):
#     password1 = request.POST.get('password1')
#     password2 = request.POST.get('password2')
#     if password1 == password2:
#         return True
#     else:
#         False


# def email_validation(request):
#     email = request.POST.get('email')
#     if User.objects.filter(email=email).exists():
#         return False
#     else:
#         return True


def sign_up_validation(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() or password1 != password2:
        return False
    else:
        return True
