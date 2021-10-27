from django.shortcuts import render, redirect

from store.interfaces.forms.user import UserCreate
from store.data.user.models import CustomUser as User
from store.data.item.models import Item


def landing_page(request):
    return render(request, "landing_page.html")


def user_creation(request):

    form = UserCreate()
    if request.method == "POST":
        form = UserCreate(request.POST)
        if form.is_valid():
            form.save(commit = False)
            User.objects.create(**form.cleaned_data)
        return redirect('landing_page')

    else:
        form = UserCreate()

    return render(request, "user/user_creation.html", {'form': form})


def main_store(request):

    all_items = Item.objects.all()

    return render(request, "store/main_store.html", {'all_items':all_items})