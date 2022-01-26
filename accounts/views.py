from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
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
from .models import Comments, RetweetTweet, UserProfile, UserPost
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
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form, 'error': errors})


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
    context["form"] = form
    # context["data"] = UserPost.objects.filter(
    #     user=request.user).order_by('-date_published')
    my_posts = UserPost.objects.filter(
        user=request.user)
    # posts_of_followers = UserPost.objects.exclude(follower__in=request.user)
    # follows_users = request.user.userprofile.follower.all()
    # follows_posts = UserPost.objects.filter(__in=follows_users)
    followers = []
    z = UserProfile.objects.raw('select * from accounts_userprofile_follower')
    for i in z:
        if i.user_id == request.user.id:
            followers.append(UserProfile.objects.get(id=i.userprofile_id))
    print("Numbers: ", followers)
    context["follo"] = followers
    # for people in followers:
    #     print(people.user)
    if len(followers) != 0:
        all_posts = UserPost.objects.filter(
            user__in=[people.user for people in followers]
        ).union(my_posts).order_by('-date_published')
        context["data"] = all_posts

    # for i in all_posts:
    #     print(i.user.userprofile.profile_pic)
    # print(all_posts)

    return render(request, "accounts/dashboard.html", context)


@login_required
def profile(request):
    user_post = {}
    user_post["data"] = UserPost.objects.filter(
        user=request.user).order_by('-date_published')

    # Getting follower count
    post = get_object_or_404(UserProfile, user=request.user.id)
    total_followers = post.number_of_followers()
    user_post["followers"] = total_followers

    # Getting following count
    following = post.number_of_following(request.user.id)
    print("Users following", following)
    user_post["following"] = following
    return render(request, "accounts/profile.html", user_post)


def users_profile(request, pk):
    user_post = {}
    user_id = User.objects.get(id=pk)
    retweet_post = UserPost.objects.filter(
        user_id=pk, check_retweet=True)

    tweet = UserPost.objects.filter(
        user_id=pk, check_retweet=False).union(retweet_post)
    user_post["data"] = tweet.order_by('-date_published')
    user_post["username"] = user_id
    post = get_object_or_404(UserProfile, user=pk)
    total_followers = post.number_of_followers()
    user_post["followers"] = total_followers
    print(user_post)
    following = post.number_of_following(pk)
    print("Users following", following)
    user_post["following"] = following

    # user_post["data"] = UserPost.objects.filter(
    #     user_id=pk).order_by('-date_published')
    # user_post["username"] = user_id
    # post = get_object_or_404(UserProfile, user=pk)
    # total_followers = post.number_of_followers()
    # user_post["followers"] = total_followers
    # print(user_post)
    # following = post.number_of_following(pk)
    # print("Users following", following)
    # user_post["following"] = following

    return render(request, 'accounts/profile_user.html', user_post)


# Delete the post
@login_required
def post_delete(request, pk):
    obj = get_object_or_404(UserPost, id=pk)
    obj.delete()
    return redirect("profile")

@login_required
def comment_delete(request, pk):
    obj = get_object_or_404(Comments, id=pk)
    obj.delete()
    return redirect("profile")

# Profile Edit
@login_required
def profile_edit(request):
    form = ProfileForm(instance=request.user.userprofile)
    form2 = EditRegister(instance=request.user)
    if request.method == "POST":
        form = ProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        form2 = EditRegister(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form2.save()

            return redirect("profile")
    context = {"form": form,
               "form2": form2
               }

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
            return redirect("profile")
    context = {"form": form}

    return render(request, "accounts/post.html", context)


def search_users(request):
    search_result = {}
    search_term = request.GET.get("search", None)
    if search_term:
        user_list = User.objects.filter(
            Q(first_name__icontains=search_term)
            | Q(last_name__icontains=search_term)
            | Q(first_name__icontains=search_term)
            | Q(username__icontains=search_term)
        )
        posts = UserPost.objects.filter(tweet_post__icontains = search_term)
        print(posts)
        search_result = {"user_list": user_list, "posts": posts}

    return render(
        request,
        "accounts/search_users.html",
        search_result
    )


@login_required
def post_detail(request, pk):
    obj = UserPost.objects.get(id=pk)
    print(obj)
    post = get_object_or_404(UserPost, id=pk)
    # total_likes = post.number_of_likes()
    # print(total_likes)

    form = CommentsForm()
    if request.method == "POST":
        form = CommentsForm(request.POST, request.FILES or None)
        if form.is_valid():
            if form.cleaned_data != {}:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.user_post = obj
                instance.save()
            return redirect("./"+str(pk))

    comments = Comments.objects.filter(user_post=obj).order_by("-created_on")
    for i in comments:
        print(i)
    context = {"form": form, "tweet": obj,
               "comments": comments}
    return render(request, "accounts/post_detail.html", context)


@login_required
def liked_post(request, pk):
    # obj = UserPost.objects.get(id=pk)
    post = get_object_or_404(UserPost, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        post.check_like = False
        post.save()
    else:
        post.likes.add(request.user)
        post.check_like = True
        post.save()
    post = get_object_or_404(UserPost, id=pk)
    total_likes = post.number_of_likes()
    print(request.path)
    # return render(request, request.path, {"likes_count": total_likes})
    # location =  request.POST.page
    # print(location)
    if request.method == 'POST':
        request.POST.get('page')
        link = (request.POST.get('page'))
    print("yea",link)
    # return HttpResponseRedirect(reverse('dashboard'))
    return redirect(link)


@login_required
def follow(request, pk):
    user_visited = User.objects.get(id=pk)
    user = request.user
    print("Follower: ", user_visited, pk)
    user_visited_data = get_object_or_404(UserProfile, user=pk)
    following = user.follow.all()
    print(user_visited_data)
    print("Following:", len(following))
    if user_visited_data.follower.filter(id=request.user.id).exists():
        user_visited_data.follower.remove(request.user)
        user_visited_data.follow_check = "Follow"
        user_visited_data.save()
    else:
        user_visited_data.follower.add(request.user)
        user_visited_data.follow_check = "Unfollow"
        user_visited_data.save()

    total_followers = user_visited_data.number_of_followers()
    print("Followers:", total_followers)
    # total_following = post.number_of_following()
    # print("Following:", total_following)

    # following_table = UserFollowing.objects.create(user=user,followers=user_visited)
    # print(len(following))

    # following = UserFollowing.objects.all()

    # authorObj = User.objects.get(username=author)
    # currentUserObj = User.objects.get(username=request.user.username)
    # st(following)
    # context = {"followers": total_followers}
    return redirect("../profile_user/"+str(pk))
    # return HttpResponseRedirect(reverse('profile_user',args=[str(pk)]))
    # return redirect(request, 'accounts/profile_user.html',context)
    # return HttpResponseRedirect(reverse('post_detail',args=[str(pk)],))


@login_required
def retweet(request, pk):
    tweet = UserPost.objects.filter(id=pk)
    tweet_data = UserPost.objects.get(id=pk)
    print(tweet)
    print(request.user)
    if tweet_data.check_retweet == True:
        UserPost.objects.filter(id=pk).delete()
        
    else:
        for i in tweet:
            new_retweet = UserPost.objects.create(
            retweet=tweet_data, retweet_user_id=tweet_data.user, user=request.user, tweet_post=i.tweet_post, date_published=i.date_published, img=i.img, check_retweet=True)
    
    if request.method == 'POST':
        request.POST.get('page')
        link = (request.POST.get('page'))
    print("yrtew", link)
    # Retweet issue1
    # RetweetTweet.objects.create(retweet=tweet_data, user=request.user)
    
    return redirect(link)
    


def comments(request, pk):
    form = CommentsForm()
    obj = UserPost.objects.get(id=pk)
    if request.method == "POST":
        form = CommentsForm(request.POST, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.user_post = obj
            instance.save()
