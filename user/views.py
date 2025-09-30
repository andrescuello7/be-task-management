# user/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from .models import User, AuthToken

@api_view(['POST'])
def create_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not username or not password:
        return Response({"error": "username y password son obligatorios"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "El usuario ya existe"}, status=400)

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password),
        first_name=first_name,
        last_name=last_name
    )

    token = AuthToken.objects.create(user=user)
    return Response({"message": "Usuario creado", "token": token.key})


@api_view(['POST'])
def auth_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=404)

    if not check_password(password, user.password):
        return Response({"error": "Credenciales inválidas"}, status=400)

    token, _ = AuthToken.objects.get_or_create(user=user)
    return Response({"token": token.key})


@api_view(['GET'])
def get_user_by_token(request):
    token_key = request.headers.get("Authorization")
    if not token_key:
        return Response({"error": "Token requerido"}, status=401)

    try:
        token = AuthToken.objects.get(key=token_key.replace("Token ", ""))
    except AuthToken.DoesNotExist:
        return Response({"error": "Token inválido"}, status=401)

    user = token.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "created_at": user.created_at,
    })


@api_view(['GET'])
def get_all_users(request):
    token_key = request.headers.get("Authorization")
    if not token_key:
        return Response({"error": "Token requerido"}, status=401)

    try:
        token = AuthToken.objects.get(key=token_key.replace("Token ", ""))
    except AuthToken.DoesNotExist:
        return Response({"error": "Token inválido"}, status=401)

    auth_user = token.user
    users = User.objects.all()

    data = []
    for u in users:
        data.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "created_at": u.created_at,
        })

    return Response({
        "request_user": {
            "id": auth_user.id,
            "username": auth_user.username
        },
        "users": data
    })