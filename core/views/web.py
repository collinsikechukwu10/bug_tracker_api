from django.contrib.auth import get_user_model, logout, get_user
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from django.views.decorators.http import require_GET, require_http_methods
from core.forms import LoginForm, RegisterForm

User = get_user_model()


@login_required()
@require_GET
def home(request):
    return render(request, "core/index.html", {})


@require_http_methods(["GET", "POST"])
def auth_login(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        next_ = request.POST.get("next", "/")
        print(form.is_valid())
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            remember_me = form.cleaned_data['remember_me']
            if remember_me:
                request.session.set_expiry(0)
                request.session.modified = True
            return redirect(next_)
        else:
            return render(request, "core/login.html", dict(form=form, next=next_))
    elif request.method == "GET":
        next_ = request.GET.get("next", "/")
        user = get_user(request)
        if user.is_authenticated:
            return redirect(next_)
        else:
            form = LoginForm(request)
            return render(request, "core/login.html", dict(form=form, next=next_))


@login_required()
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "GET":
        form = RegisterForm(request)
        return render(request, "core/register.html", {"form": form})
    elif request.method == "POST":
        form = RegisterForm(request, request.POST)
        if form.is_valid():
            obj = form.save()
            redirect("core_users_page")
        else:
            return render(request, "core/register.html", {"form": form})


@login_required()
@user_passes_test(lambda u: u.is_superuser)
@require_GET
def users_page(request):
    return render(request, "core/users_list.html", {"users": User.get_users()})


@login_required()
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def update_user(request, pk):
    pass


@login_required()
@require_GET
def auth_logout(request):
    logout(request)
    return redirect(settings.LOGIN_URL)
