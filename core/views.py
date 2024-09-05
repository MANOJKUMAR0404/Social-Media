from django.shortcuts import render , redirect
from django.contrib.auth.models import User ,auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,Likepost,FollowersCount
from itertools import chain
import random
# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_obj = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_obj)

    user_following_list =[]
    user_feed =[]
    user_following = FollowersCount.objects.filter(follower = request.user.username)
    for user in user_following:
        user_following_list.append(user.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user = usernames)
        user_feed.append(feed_lists)

    feed_list = list(chain(*user_feed))

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    return render(request,'core/index.html',{'user':user_profile,'posts':feed_list,'suggestions_username_profile_list':suggestions_username_profile_list[:4]})

@login_required(login_url='signin')
def home(request):
    user_obj = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_obj)

    user_following_list =[]
    user_feed =[]
    user_following = FollowersCount.objects.filter(follower = request.user.username)
    for user in user_following:
        user_following_list.append(user.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user = usernames)
        user_feed.append(feed_lists)

    feed_list = list(chain(*user_feed))

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    return render(request,'core/index2.html',{'user':user_profile,'posts':feed_list,'suggestions_username_profile_list':suggestions_username_profile_list[:4]})


@login_required(login_url='signin')
def upload(request):
    user_obj = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_obj)

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()

        return redirect('home2')
    else:
        return render(request,'core/addpost.html',{'user':user_profile})

@login_required(login_url='signin')
def search(request):
    user_object =User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user = user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object =User.objects.filter(username__icontains=username)

        username_profile =[]
        username_profile_list =[]

        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_list = Profile.objects.filter(id_user =ids)
            username_profile_list.append(profile_list)
        username_profile_list = list(chain(*username_profile_list))



        context={'user_profile':user_profile,'username_profile_list':username_profile_list}
    return render(request,'core/search.html',context)

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id = post_id)
    like_filter = Likepost.objects.filter(post_id = post_id,username=username).first()

    if like_filter == None :
        new_like = Likepost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_likes = post.no_likes+1
        post.save()
        return redirect('home2')
    else:
        like_filter.delete()
        post.no_likes = post.no_likes-1
        post.save()
        return redirect('home2')
    
@login_required(login_url='signin')
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user = user_object)
    user_post = Post.objects.filter(user = pk)
    post_length = len(user_post)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower = follower,user = user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    
    follower = len(FollowersCount.objects.filter(user = pk))
    following = len(FollowersCount.objects.filter(follower = pk))

    context ={'user_object':user_object,'user_profile':user_profile,'user_post':user_post,'post_length':post_length,'button_text':button_text,"follower":follower,"following":following}
    return render(request,'core/profile.html',context)

@login_required(login_url='signin')
def profile2(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user = user_object)
    user_post = Post.objects.filter(user = pk)
    post_length = len(user_post)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower = follower,user = user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    
    follower = len(FollowersCount.objects.filter(user = pk))
    following = len(FollowersCount.objects.filter(follower = pk))

    context ={'user_object':user_object,'user_profile':user_profile,'user_post':user_post,'post_length':post_length,'button_text':button_text,"follower":follower,"following":following}
    return render(request,'core/profile2.html',context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower,user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile2/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile2/'+user)
    else:
        return redirect("/")
    
@login_required(login_url='signin')
def setting(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')

    return render(request,'core/setting.html',{'user_profile':user_profile})
    
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already registered')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()

                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)

                user_model =User.objects.get(username=username)
                new_user=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_user.save()
                return redirect('settings')

        else:
            messages.info(request,"Password Mismatch")
            return redirect('signup')
    return render(request,'core/signup.html')
    
def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home2')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('signin')
    return render(request,'core/signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')