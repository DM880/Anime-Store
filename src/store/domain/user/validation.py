from store.data.user.models import CustomUser as User


def sign_up_validation(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() or password1 != password2:
        return False
    else:
        return True
