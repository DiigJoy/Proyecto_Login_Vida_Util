import paramiko
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

@csrf_protect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
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