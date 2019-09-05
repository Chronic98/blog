from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.models import Group


def redirect_login(request):
    return redirect('login_user_url', permanent=True)

def home_page(request):
    group = Group.objects.all()
    return render(request, 'base.html')

def redirect_blog(request):
    return redirect('post_list_url', permanent=True)
