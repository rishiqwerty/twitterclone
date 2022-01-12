from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import (
    EditRegister,
    LoginForm,
    CreateRegisterForm,
    ProfileForm,
    UserPostForm,
    CommentsForm,
)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Comments, UserProfile, UserPost
from django.db.models import Q

# Create your views here.


def user_login(request):
    errors = ''
    if request.user.is_authenticated:
        return redirect("dashboard")

    elif request.method == "POST":
        form = LoginForm(request.POST)
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('dashboard')

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("dashboard")
                else:
                    
                    return HttpResponse("Disabled account")
            errors = '*Invalid Username/Password'

        else:
            # print("Error")
            form = LoginForm()
            errors = '*You might have missed typing username/password'
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form":form, 'error': errors})


def user_register(request):

    form = CreateRegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        profile = UserProfile.objects.create(user=user)
        new_user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(request, new_user)
        return redirect("profile_edit")
    else:
        print(form.errors)
        context = {"form": form.errors}
    return render(request, "accounts/registration.html", context)


def user_logout(request):
    logout(request)
    # try:
    #     del request.session['user']
    # except:
    #     return render(request, "accounts/logout.html")
    return render(request, "accounts/logout.html")


@login_required
def dashboard(request):
    form = UserPostForm(request.POST, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            return redirect(".")
    context = {"section": "dashboard"}
    context ["form"] = form
    context["data"] = UserPost.objects.filter(user=request.user).order_by('-date_published')
    return render(request, "accounts/dashboard.html", context)


@login_required
def profile(request):
    user_post = {}
    user_post["data"] = UserPost.objects.filter(user=request.user)
    print(UserPost.objects.filter(user=request.user))

    return render(request, "accounts/profile.html", user_post)


def users_profile(request, pk):
    user_post = {}
    user_id = User.objects.get(id=pk)
    user_post["data"] = UserPost.objects.filter(user_id=pk).order_by('-date_published')
    user_post["username"] = user_id
    print(user_post)


    return render(request, 'accounts/profile_user.html',user_post)



# Delete the post
@login_required
def post_delete(request, pk):
    obj = get_object_or_404(UserPost, id=pk)
    obj.delete()
    return redirect("profile")


# Profile Edit
@login_required
def profile_edit(request):
    form = ProfileForm(instance=request.user.userprofile)
    form2 = EditRegister(instance= request.user)
    if request.method == "POST":
        form = ProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        form2 = EditRegister(request.POST, instance=request.user)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
        
            return redirect("profile")
    context = {"form": form,
                "form2": form2}

    return render(request, "accounts/profile_edit.html", context)


@login_required
def user_posts_form(request):
    form = UserPostForm(request.POST, request.FILES or None)
    if request.method == "POST":
        # form = UserPostForm(request.POST, request.FILES or None)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            return redirect("../")
    context = {"form": form}

    return render(request, "accounts/post.html", context)


def search_users(request):
    search_result = {}
    search_term = request.GET.get("search", None)
    if search_term:
        user_list = User.objects.filter(
            Q(first_name__icontains=search_term)
            | Q(last_name__icontains=search_term)
            | Q(username__icontains=search_term)
        )
        search_result = {"user_list": user_list}
    
    return render(
        request,
        "accounts/search_users.html",
        search_result
    )


@login_required
def post_detail(request, pk):
    obj = UserPost.objects.get(id=pk)
    print(obj)
    form = CommentsForm(request.POST, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.user_post = obj
            instance.save()
            return redirect("./"+str(pk))
    comments = Comments.objects.filter(user_post=obj).order_by("-created_on")
    for i in comments:
        print(i)
    context = {"form": form, "tweet": obj, "comments":comments}
    return render(request, "accounts/post_detail.html", context)

# @login_required
# def liked_post(request, pk):
#     obj = UserPost.objects.get(id=pk)