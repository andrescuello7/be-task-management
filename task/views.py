from .models import Task
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_tasks(request):
    tasks = Task.objects.filter(author=request.user).order_by("-created_at")
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_task(request):
    title = request.data.get("title")
    description = request.data.get("description")
    status_ = request.data.get("status", "pending")

    if not title or not description:
        return Response({"error": "Faltan campos obligatorios"}, status=400)

    task = Task.objects.create(
        title=title,
        description=description,
        status=status_,
        author=request.user
    )

    return Response({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": task.created_at,
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_filter_search(request):
    search = request.GET.get("search")
    date = request.GET.get("date")
    tasks = Task.objects.all()
    
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def find_task_by_date(request):
    date_str = request.data.get("date")
    if not date_str:
        return Response({"error": "Debes enviar una fecha (YYYY-MM-DD)"}, status=400)

    try:
        date = parse_date(date_str)
    except Exception:
        return Response({"error": "Formato de fecha inválido"}, status=400)

    tasks = Task.objects.filter(author=request.user, created_at__date=date)

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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_task(request):
    task_id = request.data.get("id")
    if not task_id:
        return Response({"error": "Debes enviar el id de la tarea"}, status=400)

    try:
        task = Task.objects.get(id=task_id, author=request.user)
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_task(request):
    task_id = request.data.get("id")
    if not task_id:
        return Response({"error": "Debes enviar el id de la tarea"}, status=400)

    try:
        task = Task.objects.get(id=task_id, author=request.user)
        task.delete()
        return Response({"message": "Tarea eliminada correctamente"})
    except Task.DoesNotExist:
        return Response({"error": "Tarea no encontrada"}, status=404)
