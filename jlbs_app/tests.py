# jlbs_app/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Crear un usuario de prueba
        user = User.objects.create_user(username='testuser', password='12345')

        # Enviar una solicitud POST para hacer login
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        
        # Verificar si el login fue exitoso
        self.assertEqual(response.status_code, 302)  # Redirección tras login exitoso
        self.assertRedirects(response, reverse('home'))  # Asegurarse de que redirige al 'home'

        # Verificar si el usuario está autenticado
        self.assertTrue('_auth_user_id' in self.client.session)
