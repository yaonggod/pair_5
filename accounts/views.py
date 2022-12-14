from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def index(request):
    users = get_user_model().objects.all()
    context = {'users' : users}
    return render(request, 'accounts/index.html', context)

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {'form' : form}
    return render(request, 'accounts/signup.html', context)

def detail(request, user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    context = {'user' : user}
    return render(request, 'accounts/detail.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:index')
    else:
        form = AuthenticationForm()
    context = {'form' : form}
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('accounts:index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form' : form,}
    return render(request, 'accounts/update.html', context)

@ login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # ?????? ?????? ??? ????????? ????????? ?????? ????????? ?????? ??????, ??? ?????? ????????? ????????????
            # from django.contrib.auth import update_session_auth_hash
            # update_session_auth_hash(request, form.user)
            return redirect('accounts:login')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form, }
    return render(request, 'accounts/change_password.html', context)

@ login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('articles:index') 

@login_required
def follow(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.user == user:
        messages.warning(request, '????????? ????????? ??? ??? ????????????.')
        return redirect('accounts:index')
    if request.user in user.followers.all():
        user.followers.remove(request.user)
        is_followed = False
    else:
        user.followers.add(request.user)
        is_followed = True
    context = {'isfollowed': is_followed, 'followCount': user.followers.count()}
    return JsonResponse(context)
