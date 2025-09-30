from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from task.models import Task

User = get_user_model()

class TaskViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="4ndres_cuello",
            email="andyexample@gmail.com",
            password="admin1",
            first_name="Andy",
            last_name="Cuello"
        )
        
        data = {
            "username": "4ndres_cuello",
            "password": "admin1"
        }
        auth = self.client.post("/api/user/auth", data, content_type="application/json")
        self.headers = {
            "Authorization": auth.json()["token"],
            "Content-Type": "application/json",
        }
        
        self.task = Task.objects.create(
            title="Tarea de deploy",
            description="Deploy en aws para pruebas de STG",
            status="TODO",
            author=self.user, 
            created_at=timezone.now()
        )

    def test_get_all_tasks(self):
        url = "/api/tasks/getAll"
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_task(self):
        url = "/api/tasks/create"
        data = {
            "title": "Tarea de deploy",
            "description": "Deploy en aws para pruebas de STG",
            "status": "IN_PROGRESS",
        }
        response = self.client.post(url, data, content_type="application/json", headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)

    def test_filter_by_search(self):
        url = "/api/tasks/search?search=deploy"
        response = self.client.get(url, content_type="application/json", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_change_task(self):
        url = "/api/tasks/change"
        data = {"id": self.task.id, "title": "Nuevo título"}
        response = self.client.put(url, data, content_type="application/json", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Nuevo título")

    def test_delete_task(self):
        url = "/api/tasks/delete"
        data = {"id": self.task.id}
        response = self.client.delete(url, data, content_type="application/json", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)
