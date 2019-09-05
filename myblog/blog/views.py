from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *


def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    post_in_page = 10
    paginator = Paginator(posts, post_in_page)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'blog/index.html', context=context)


class PostDetail(ObjectDetailMixim, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixim, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = False


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixim, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = False


class PostDelete(LoginRequiredMixin, ObjectDeleteMixim, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'post_list_url'
    raise_exception = False


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetailMixim, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixim, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = False


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixim, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = False


class TagDelete(LoginRequiredMixin, ObjectDeleteMixim, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = False


class Leave_comment(LoginRequiredMixin, ObjectLeaveComment, View):
    model = Post
    template = 'blog/post_detail_url_comment.html'
    redirect_url = 'post_list_url'
    raise_exception = False


@login_required
def user_logout(request):
    logout(request)
    return redirect('login_user_url')


class LoginUser(View):
    def get(self, request):
        log_user = LoginForm()
        return render(request, 'blog/identification.html', context={'log_user': log_user})

    def post(self, request):
        bound_form = LoginForm(request.POST)
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('post_list_url')
        else:
            return render(request, 'blog/identification.html', context={'log_user': bound_form})


class AddUz(View):
    def get(self, request):
        form = UzForm()
        return render(request, 'blog/uz_add.html', context={'form': form})

    def post(self, request):
        bound_form = UzForm(request.POST)

        if bound_form.is_valid():
            new_student = bound_form.save()
            return redirect('adduz_url')
        return render(request, 'blog/uz_add.html', context={'form': bound_form})

