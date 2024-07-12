import paramiko
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from axes.helpers import get_client_ip_address
from axes.models import AccessAttempt
from axes.utils import reset

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        ip_address = get_client_ip_address(request)
        
        attempts = AccessAttempt.objects.filter(username=username, ip_address=ip_address, failures_since_start__gte=settings.AXES_FAILURE_LIMIT)
        
        if attempts.exists():
            messages.error(request, 'Tu cuenta está bloqueada debido a múltiples intentos fallidos.')
            return redirect(settings.AXES_LOCKOUT_URL)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')

    return render(request, 'login.html')


@login_required
def home_view(request):
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        
        # SFTP Upload
        host = 'localhost'
        port = 2222
        username = 'sftpuser'
        password = 'password'
        remote_path = f'/upload/{filename}'
        
        try:
            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(fs.path(filename), remote_path)
            sftp.close()
            transport.close()
            messages.success(request, 'Archivo subido y enviado correctamente por SFTP.')
        except Exception as e:
            messages.error(request, f'Error al enviar el archivo por SFTP: {e}')
    
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('login')


def lockout_view(request):
    return render(request, 'lockout.html')