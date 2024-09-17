from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Follow

# Obtener el modelo de usuario actual
User = get_user_model()

def users_not_followed_by_user(request):
    current_user = request.user if request.user.is_authenticated else None

    if current_user:
        # Obtener los IDs de los usuarios que ya está siguiendo
        followed_users = Follow.objects.filter(follower=current_user).values_list('following', flat=True)
        
        # Obtener los usuarios que el usuario actual no sigue
        users_not_followed = User.objects.exclude(id__in=followed_users).exclude(id=current_user.id)
    else:
        # Si no está logueado, mostrar todos los usuarios
        users_not_followed = User.objects.all()

   
    return {'users_not_followed': users_not_followed}