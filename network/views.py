from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from .models import User, Post,Follow,Like
import json
from django.core.paginator import Paginator

def index(request):
    if request.method == 'GET':
        # Obtener todas las publicaciones ordenadas por timestamp
        posts = Post.objects.all().order_by('-timestamp')
        
        # Obtener el usuario actual si está autenticado
        user = request.user if request.user.is_authenticated else None
        
        # Si el usuario está autenticado, obtener sus seguidores
        if user:
            following = Follow.objects.filter(follower=user).values_list('following', flat=True)
        else:
            following = []
        
        # Serializar las publicaciones
        posts_data = []
        for post in posts:
            posts_data.append({
                "id": post.id,
                "author_id": post.author.id,
                "author": post.author.username,
                "content": post.content,
                "timestamp": post.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "likes": post.likes_count,
                'liked': Like.objects.filter(user=user, post=post).exists() if user else False,
                'following': post.author.id in following if user else False
            })
        
        # Agregar paginación
        paginator = Paginator(posts_data, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            'page_obj': page_obj,  
        })

    return render(request, "network/index.html")

@login_required
def following_posts(request):
    user = request.user

    # Obtener los IDs de los usuarios que el usuario actual sigue
    following_users = Follow.objects.filter(follower=user).values_list('following_id', flat=True)

    # Obtener todas las publicaciones de los usuarios que sigue, ordenadas por timestamp
    posts = Post.objects.filter(author__id__in=following_users).order_by('-timestamp')

    # Serializar las publicaciones con información sobre "likes" y "following"
    posts_data = []
    for post in posts:
        posts_data.append({
            "id": post.id,
            "author_id": post.author.id,
            "author": post.author.username,
            "content": post.content,
            "timestamp": post.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": post.likes_count,
            'liked': Like.objects.filter(user=user, post=post).exists(),  # Si el usuario actual ha dado "like"
            'following': post.author.id in following_users  # Si el usuario sigue al autor de la publicación
        })

    # Agregar paginación
    paginator = Paginator(posts_data, 10)  # 10 posts por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following_posts.html", {
        'page_obj': page_obj  # Pasa directamente el objeto `page_obj` a la plantilla
    })

@login_required
@require_POST
def post_create(request):
    try:
        # Obtener los datos del request
        data = json.loads(request.body)
        content = data.get('content', '')
        
        if content == '':
            return JsonResponse({"error": "Content cannot be empty."}, status=400)
        
        # Crear nueva publicación
        post = Post.objects.create(
            author=request.user,
            content=content
        )
        
        return JsonResponse({"message": "Post created successfully."}, status=201)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@login_required
@require_POST
def edit_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id, author=request.user)
        content = json.loads(request.body).get('content')
        post.content = content
        post.save()
        return JsonResponse({'success': True})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_POST
def toggle_follow(request, user_id):
    try:
        # Obtener el usuario a seguir/dejar de seguir
        user_to_follow = User.objects.get(id=user_id)

        # Verificar que no puede seguirse a sí mismo
        if request.user == user_to_follow:
            return JsonResponse({"error": "You cannot follow yourself."}, status=400)

        # Verificar si ya sigue al usuario
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)

        if created:
            # Si no lo sigue, empezar a seguirlo
            return JsonResponse({"message": "Followed successfully.", "following": True}, status=201)
        else:
            # Si ya lo sigue, entonces dejar de seguirlo
            follow.delete()
            return JsonResponse({"message": "Unfollowed successfully.", "following": False}, status=200)

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
@login_required
@require_POST
def toggle_like(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        user = request.user
       
        # Verificar si el usuario ya ha dado "me gusta" a la publicación
        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            # El usuario ya ha dado "me gusta", eliminar el like
            like.delete()
            liked = False
        else:
            # El usuario no ha dado "me gusta", agregar el like
            liked = True

        return JsonResponse({"liked": liked, "likes_count": post.likes_count})

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    following_users = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)

    # Obtener todas las publicaciones del usuario, ordenadas por timestamp
    posts = Post.objects.filter(author=user).order_by('-timestamp')
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    
    # Serializar las publicaciones con información sobre "likes" y "following"
    posts_data = []
    for post in posts:
        posts_data.append({
            "id": post.id,
            "author_id": post.author.id,
            "author": post.author.username,
            "content": post.content,
            "timestamp": post.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": post.likes_count,
            'liked': Like.objects.filter(user=request.user, post=post).exists(),  
            'following': post.author.id in following_users  
        })

    # Agregar paginación
    paginator = Paginator(posts_data, 10)  # 10 publicaciones por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Verificar si el usuario autenticado está siguiendo al usuario perfil
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    context = {
        'user_profile': user,
        'page_obj': page_obj,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following
    }
    
    return render(request, 'network/user_profile.html', context)
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
