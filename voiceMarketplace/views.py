from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        for msg in form.error_messages:
            print(form.error_messages[msg])
        return render(request=request,
                      template_name="register.html",
                      context={"form": form})
    form = UserCreationForm
    return render(request=request,
                  template_name="register.html",
                  context={"form": form})
