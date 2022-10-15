from django.shortcuts import render,redirect,HttpResponse
from django.core.mail import send_mail
from decouple import config
from django.contrib.auth.models import User

def home(request):
    return render(request,'home.html')



def cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastro.html')
        
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        confirmar_senha = request.POST.get('confirm-password')

        if not senha == confirmar_senha:
            #messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return HttpResponse('As senhas não coincidem')

        if len(username.strip()) == 0 or len(senha.strip()) == 0:
            #messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/auth/cadastro')
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            #messages.add_message(request, constants.ERROR, 'Já existe um usário com esse username')
            return HttpResponse('Já existe um usário com esse username')

        
        try:
            
            user = User.objects.create_user(username=username,
                                            email = email,
                                            password=senha)
            user.save()
            mensagem='mensagem de teste mandado no corpo do email'
            send_mail('Cadastro realizado com sucesso',mensagem,config('EMAIL_HOST_USER'),recipient_list=[email,'precoflix@gmail.com'])
            return HttpResponse('Email enviado')

            
        except:
            #messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('cadastro')