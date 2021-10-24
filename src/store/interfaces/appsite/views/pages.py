from django.shortcuts import render, redirect

from store.interfaces.forms.user import UserCreate
from store.data.user.models import CustomUser as User


def landing_page(request):
    return render(request, "landing_page.html")


def user_creation(request):

    form = UserCreate()

    if request.method == "POST":

        if form.is_valid():

            data = form.cleaned_data()
            User.objects.create(**data)

        return redirect('landing_page')

    return render(request, "user/user_creation.html", {'form': form})