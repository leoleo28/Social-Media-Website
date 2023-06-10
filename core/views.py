from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, Comment, Room, Message, Chat_list
from itertools import chain
import random


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts
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

    commend_list=[]
    for post in feed_list:
        comments=post.get_comment.all()
        commend_list.append(comments)
    final_commend_list= list(chain(*commend_list))

    if request.method =='POST':
        post_id=request.POST['post_id']
        origin_post=Post.objects.get(id=post_id)
        text=request.POST['text']
        username = request.user.username
        new_comment=Comment.objects.create(post=origin_post, user=username, text=text)
        new_comment.save()
        ls_comments= origin_post.get_comment.all()
        return redirect('/')
    else:
        # return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})
        return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4],'final_commend_list':final_commend_list})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    button_text=''
    if follower==user:
        button_text= 'Edit Profile'
    else:
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            button_text = 'Unfollow'
        else:
            button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'follower':follower,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def edit(request):
    post_id = request.GET.get('post_id')
    post=Post.objects.get(id=post_id)
    commend_list=[]
    for c in post.get_comment.all():
        commend_list.append(c)
    final_commend_list= list(commend_list)
    return render(request,'edit.html',{"post":post,"final_commend_list":final_commend_list})
  
@login_required(login_url='signin')
def chat(request):
    username = request.user.username
    chat_with = request.GET.get('with')
    user_chat_with = User.objects.get(username=chat_with)
    profile_chat_with = Profile.objects.get(user=user_chat_with)
    a=''
    b=''
    if username<chat_with:
        a=username
        b=chat_with
    else:
        a=chat_with
        b=username
    room=a+'_'+b
    chat_room = Room.objects.filter(name=room).first()
    if chat_room==None:
        chat_room=Room.objects.create(name=room)
        chat_room.save()
        chat_contact=Chat_list.objects.create(user=username, contact=chat_with)
        chat_contact2=Chat_list.objects.create(user=chat_with, contact=username)
        chat_contact.save()
        chat_contact2.save()
    
    all_contact=Chat_list.objects.filter(user=username)
    all_contact_profile=[]
    for c in all_contact:
        contact_user = User.objects.get(username=c.contact)
        contact_profile = Profile.objects.get(user=contact_user)
        all_contact_profile.append(contact_profile)
    
    context={
        'chat_room':chat_room,
        'username':username,
        'profile_chat_with':profile_chat_with,
        'all_contact_profile':all_contact_profile
    }

    return render(request, 'chat.html', context)

@login_required(login_url='signin')
def send(request):
    user=request.POST['username']
    person_chatwith=request.POST['person_chatwith']
    message=request.POST['message']
    a=''
    b=''
    if user<person_chatwith:
        a=user
        b=person_chatwith
    else:
        a=person_chatwith
        b=user
    room_name=a+'_'+b
    new_message=Message.objects.create(value=message, user=user, room=room_name)
    new_message.save()
    return HttpResponse('Message send successfully')

@login_required(login_url='signin')
def getmessage(request, room):
    messages=Message.objects.filter(room=room)
    cur_user=request.user.username
    if messages!=None:
        return JsonResponse({"messages":list(messages.values()),"cur_user":cur_user})
    else:
        return JsonResponse('no message')

@login_required(login_url='signin')
def edit_post(request):
    post_id = request.GET.get('post_id')
    cur_post=Post.objects.get(id=post_id)
    user=request.user.username
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = cur_post.image
            new_caption = request.POST['caption']
            cur_post.caption=new_caption
            cur_post.image=image            
            cur_post.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            new_caption = request.POST['caption']
            cur_post.caption=new_caption
            cur_post.image=image            
            cur_post.save()

        return redirect('/profile/'+user)  
    return render(request, 'edit.html', {"cur_post":cur_post, "user":user})
    

@login_required(login_url='signin')
def delete_post(request):
    user=request.user.username
    post_id = request.GET.get('post_id')
    del_post=Post.objects.get(id=post_id)
    del_post.delete()
    return redirect('/profile/'+user)
    