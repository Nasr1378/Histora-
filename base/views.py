from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Post, Topic, Comment, User,File
from .forms import PostForm, UserForm, MyUserCreationForm, FileForm



def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(
        Q(topic__name__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    post_count = posts.count()
    post_comment = Comment.objects.filter(
        Q(post__topic__name__icontains=q))[0:3]

    context = {'posts': posts, 'topics': topics,
               'post_count': post_count, 'post_comments': post_comment}
    return render(request, 'base/home.html', context)


def post(request, pk):
    post = Post.objects.get(id=pk)
    post_comments = post.comment_set.all()
    post_files = File.objects.filter(post=post)
    
    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
        # post.participants.add(request.user)
        return redirect('post', pk=post.id)

    context = {'post': post, 'post_comments': post_comments,'post_files': post_files,
               }
    return render(request, 'base/post.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    post_comment = user.comment_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'posts': posts,
               'post_comments': post_comment, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    topics = Topic.objects.all()
    file_form = FileForm()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # file_form=FileForm(request.POST,request.FILES)

        # if file_form.is_valid():
        #     file_form.save()

        post=Post.objects.create(
            host=request.user,
            topic=topic,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
        )
        
        file_form=FileForm(request.POST,request.FILES,instance=post)

        if file_form.is_valid():
            file_form.save()
        
        return redirect('home')

    context = {'form': form, 'topics': topics, 'file_form': file_form}
    return render(request, 'base/post_form.html', context)


@login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    file_form = FileForm(instance=post)
    topics = Topic.objects.all()
    if request.user != post.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        post.title = request.POST.get('title')
        post.topic = topic
        post.description = request.POST.get('description')
        post.save()
        file_form=FileForm(request.POST,request.FILES,instance=post)

        if file_form.is_valid():
            file_form.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'post': post,'file_form':file_form}
    return render(request, 'base/post_form.html', context)


@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)

    if request.user != post.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': post})


@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': comment})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    post_comment = Comment.objects.all()
    return render(request, 'base/activity.html', {'post_comments': post_comment})
