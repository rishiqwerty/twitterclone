from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CreateRegisterForm, ProfileForm, UserPostForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserPost

# Create your views here.


def user_login(request):
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

        else:
            # print("Error")
            form = LoginForm()
    return render(request, "accounts/login.html")


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
    context = {"form": form}
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
    context = {
        "section": "dashboard"
    }
    context['data'] = UserPost.objects.filter(user=request.user)
    return render(request, "accounts/dashboard.html", context)


@login_required
def profile(request):
    user_post = {}
    user_post['data'] = UserPost.objects.filter(user=request.user)
    print(UserPost.objects.filter(user=request.user))
    # user = UserProfile.objects.all()
    # acco = request.user.userprofile.all()
    # print(acco)
    # if request.method=='POST':
    #     form = UserProfile(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("dashboard")
    #     else:
    #         form = UserProfile()
    return render(request, "accounts/profile.html", user_post)


# Profile Edit
@login_required
def profile_edit(request):
    form = ProfileForm(instance=request.user.userprofile)
    if request.method == "POST":
        form = ProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if form.is_valid():
            form.save()
            return redirect("profile")
    context = {"form": form}

    return render(request, "accounts/profile_edit.html", context)

@login_required
def user_posts_form(request):
    form = UserPostForm(request.POST, request.FILES or None)
    if request.method == "POST":
        form = UserPostForm(
            request.POST, request.FILES or None
        )
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            return redirect("../")
    context = {"form": form}

    return render(request, "accounts/post.html", context)
