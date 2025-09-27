from .models import Task
from user.models import AuthToken
from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status


def get_user_from_token(request):
    token_key = request.headers.get("Authorization")
    if not token_key:
        return None, Response({"error": "Token requerido"}, status=401)

    try:
        token = AuthToken.objects.get(key=token_key.replace("Token ", ""))
        return token.user, None
    except AuthToken.DoesNotExist:
        return None, Response({"error": "Token inválido"}, status=401)


@api_view(['GET'])
def get_all_tasks(request):
    user, error = get_user_from_token(request)
    if error:
        return error

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
                "firstname": t.author.firstname,
                "lastname": t.author.lastname,
            },
        }
        for t in tasks
    ]
    return Response(data)


@api_view(['POST'])
def create_task(request):
    user, error = get_user_from_token(request)
    if error:
        return error

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
def find_task_by_date(request):
    user, error = get_user_from_token(request)
    if error:
        return error

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
                "firstname": t.author.firstname,
                "lastname": t.author.lastname,
            },
        }
        for t in tasks
    ]

    return Response(data)


@api_view(['PUT'])
def change_task(request):
    user, error = get_user_from_token(request)
    if error:
        return error

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
    user, error = get_user_from_token(request)
    if error:
        return error

    task_id = request.data.get("id")
    if not task_id:
        return Response({"error": "Debes enviar el id de la tarea"}, status=400)

    try:
        task = Task.objects.get(id=task_id, author=user)
        task.delete()
        return Response({"message": "Tarea eliminada correctamente"})
    except Task.DoesNotExist:
        return Response({"error": "Tarea no encontrada"}, status=404)
