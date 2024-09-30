from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BlogPost
from .forms import BlogPostForm
import json
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'success': False, 'error': 'Invalid username or password'}), content_type='application/json')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    posts = BlogPost.objects.all()
    return render(request, 'home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'success': False, 'error': 'Invalid form data'}), content_type='application/json')
    else:
        form = BlogPostForm()
        return render(request, 'create_post.html', {'form': form})

@login_required
def ajax_create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'success': False, 'error': 'Invalid form data'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False, 'error': 'Invalid Request type'}),
                            content_type='application/json')

@login_required
def edit_post(request, pk):
    post = BlogPost.objects.get(pk=pk)
    if request.method == 'POST':
        if post.author == request.user:
            form = BlogPostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return HttpResponse(json.dumps({'success': True}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'success': False, 'error': 'Invalid form data'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'success': False, 'error': 'You can edit your blogs only.'}),
                                content_type='application/json')
    else:
        form = BlogPostForm(instance=post)
        return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def ajax_edit_post(request, pk):
    post = BlogPost.objects.get(pk=pk)
    if request.method == 'POST':
        if post.author == request.user:
            form = BlogPostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return HttpResponse(json.dumps({'success': True}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'success': False, 'error': 'Invalid form data'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'success': False, 'error': 'You can edit your blogs only.'}),
                                content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False, 'error': 'Invalid Request type'}),
                            content_type='application/json')


@login_required
def ajax_delete_post(request, pk):
    if request.method == 'DELETE':
        post = BlogPost.objects.get(pk=pk)
        if post.author == request.user:
            post.delete()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'success': False, 'error': 'You can delete your blogs only.'}),
                                content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False, 'error': 'Invalid Request type'}),
                            content_type='application/json')
