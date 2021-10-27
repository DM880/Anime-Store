from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic as generic_views

from store.interfaces.forms.user import UserCreate
from store.data.user.models import CustomUser as User
from store.data.item.models import Item


class LandingPage(generic_views.TemplateView):
    template_name = "landing_page.html"


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('main_store')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('main_store')

        else:
            return render(request, "user/sign_in.html", {'error':True})

    else:
        return render(request, "user/sign_in.html")


def signup(request):
    form = UserCreate()

    if request.method == "POST":
        form = UserCreate(request.POST)
        if form.is_valid():
            form.save(commit = False)
            User.objects.create(**form.cleaned_data)
        return redirect('landing_page')

    else:
        form = UserCreate()

    return render(request, "user/signup.html", {'form': form})


def main_store(request):
    all_items = Item.objects.all()

    return render(request, "store/main_store.html", {'all_items':all_items})


