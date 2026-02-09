from django.contrib import messages
from django.shortcuts import redirect, render

from pessoas.models import Colaborador


def public_home(request):
    return render(request, "public/home.html")


def colaborador_cadastro(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip().lower()
        senha = request.POST.get("senha", "")
        profissao = request.POST.get("profissao", "").strip()

        erros = []
        if not nome:
            erros.append("Informe o nome.")
        if not email:
            erros.append("Informe o e-mail.")
        if not senha:
            erros.append("Informe a senha.")
        if not profissao:
            erros.append("Informe a profissao.")
        if email and Colaborador.objects.filter(email=email).exists():
            erros.append("Ja existe um colaborador com este e-mail.")

        if erros:
            for erro in erros:
                messages.error(request, erro)
        else:
            colaborador = Colaborador(nome=nome, email=email, profissao=profissao)
            colaborador.set_senha(senha)
            colaborador.save()
            messages.success(request, "Cadastro realizado com sucesso.")
            return redirect("colaborador_cadastro")

    return render(request, "public/cadastro.html")
