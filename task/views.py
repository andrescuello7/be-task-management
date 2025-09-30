from user.models import AuthToken
from .models import Task
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def get_all_tasks(request):
    token_key = request.headers.get("Authorization")
    if not token_key:
        return Response({"error": "Token requerido"}, status=401)

    try:
        if token_key.startswith("Token "):
            token_key = token_key.replace("Token ", "")
        token = AuthToken.objects.get(key=token_key)
    except AuthToken.DoesNotExist:
        return Response({"error": "Token inválido"}, status=401)
    
    user = token.user
    tasks = Task.objects.filter(author=user).order_by("-created_at")
    data = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "created_at": t.created_at,
            "author": {
                "id": t.author.id,
                "username": t.author.username,
                "email": t.author.email,
                "first_name": t.author.first_name,
                "last_name": t.author.last_name,
            },
        }
        for t in tasks
    ]
    return Response(data)


@api_view(['POST'])
def create_task(request):
    token_key = request.headers.get("Authorization")
    if not token_key:
        return Response({"error": "Token requerido"}, status=401)

    try:
        if token_key.startswith("Token "):
            token_key = token_key.replace("Token ", "")
        token = AuthToken.objects.get(key=token_key)
    except AuthToken.DoesNotExist:
        return Response({"error": "Token inválido"}, status=401)
    
    user = token.user
    title = request.data.get("title")
    description = request.data.get("description")
    status_ = request.data.get("status", "pending")

    if not title or not description:
        return Response({"error": "Faltan campos obligatorios"}, status=400)

    task = Task.objects.create(
        title=title,
        description=description,
        status=status_,
        author=user
    )

    return Response({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": task.created_at,
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_filter_search(request):
    token_key = request.headers.get("Authorization")
    if not token_key:
        return Response({"error": "Token requerido"}, status=401)

    try:
        if token_key.startswith("Token "):
            token_key = token_key.replace("Token ", "")
        token = AuthToken.objects.get(key=token_key)
    except AuthToken.DoesNotExist:
        return Response({"error": "Token inválido"}, status=401)
    
    user = token.user
    search = request.GET.get("search")
    date = request.GET.get("date")
    tasks = Task.objects.filter(author=user)
    
    if not search and not date:
        return Response({"error": "Debes enviar un Titulo o Fecha"}, status=400)

    if date:
        tasks = tasks.filter(created_at__gte=parse_date(date))

    if search:
        tasks = tasks.filter(title__icontains=search)
    
    data = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "created_at": t.created_at,
            "author": {
                "id": t.author.id,
                "username": t.author.username,
                "email": t.author.email,
                "first_name": t.author.first_name,
                "last_name": t.author.last_name,
            },
        }
        for t in tasks
    ]
    return Response(data)
    
    
@api_view(['GET'])
def find_task_by_date(request):
    token_key = request.headers.get("Authorization")
    if not token_key:
        return Response({"error": "Token requerido"}, status=401)

    try:
        if token_key.startswith("Token "):
            token_key = token_key.replace("Token ", "")
        token = AuthToken.objects.get(key=token_key)
    except AuthToken.DoesNotExist:
        return Response({"error": "Token inválido"}, status=401)
    
    user = token.user
    date_str = request.data.get("date")
    if not date_str:
        return Response({"error": "Debes enviar una fecha (YYYY-MM-DD)"}, status=400)

    try:
        date = parse_date(date_str)
    except Exception:
        return Response({"error": "Formato de fecha inválido"}, status=400)

    tasks = Task.objects.filter(author=user, created_at__date=date)

    data = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "created_at": t.created_at,
            "author": {
                "id": t.author.id,
                "username": t.author.username,
                "email": t.author.email,
                "first_name": t.author.first_name,
                "last_name": t.author.last_name,
            },
        }
        for t in tasks
    ]

    return Response(data)


@api_view(['PUT'])
def change_task(request):
    token_key = request.headers.get("Authorization")
    if not token_key:
        return Response({"error": "Token requerido"}, status=401)

    try:
        if token_key.startswith("Token "):
            token_key = token_key.replace("Token ", "")
        token = AuthToken.objects.get(key=token_key)
    except AuthToken.DoesNotExist:
        return Response({"error": "Token inválido"}, status=401)
    
    user = token.user
    task_id = request.data.get("id")
    if not task_id:
        return Response({"error": "Debes enviar el id de la tarea"}, status=400)

    try:
        task = Task.objects.get(id=task_id, author=user)
    except Task.DoesNotExist:
        return Response({"error": "Tarea no encontrada"}, status=404)

    task.title = request.data.get("title", task.title)
    task.description = request.data.get("description", task.description)
    task.status = request.data.get("status", task.status)
    task.save()

    return Response({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": task.created_at,
    })


@api_view(['DELETE'])
def delete_task(request):
    token_key = request.headers.get("Authorization")
    if not token_key:
        return Response({"error": "Token requerido"}, status=401)

    try:
        if token_key.startswith("Token "):
            token_key = token_key.replace("Token ", "")
        token = AuthToken.objects.get(key=token_key)
    except AuthToken.DoesNotExist:
        return Response({"error": "Token inválido"}, status=401)
    
    user = token.user
    task_id = request.data.get("id")
    if not task_id:
        return Response({"error": "Debes enviar el id de la tarea"}, status=400)

    try:
        task = Task.objects.get(id=task_id, author=user)
        task.delete()
        return Response({"message": "Tarea eliminada correctamente"})
    except Task.DoesNotExist:
        return Response({"error": "Tarea no encontrada"}, status=404)
