from store.data.user.models import CustomUser as User


def sign_up_validation(username, email, password1, password2):

    if User.objects.filter(username=username).exists():
        return f"{username} - Username already exist"

    elif User.objects.filter(email=email).exists():
        return f"{email} - Email already exist"

    elif password1 != password2:
        return "Passwords don't match"

    return True
