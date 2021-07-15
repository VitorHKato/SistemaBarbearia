from django.shortcuts import render
from django.views import View

import core.models


class Home(View):
    def get(self, *args, **kwargs):

        lista_horarios = list(core.models.Horario.objects.filter(status=True))

        context = {
            'Titulo': "Bem vindo à Barber's!.",
            'lista_horarios': lista_horarios,
        }

        return render(request=self.request, template_name='index.html', context=context)

class GerenciarFuncionarios(View):
    def get(self, *args, **kwargs):

        context = {

        }

        return render(request=self.request, template_name='gerenciar_funcionarios.html', context=context)

class GerenciarServicos(View):
    def get(self, *args, **kwargs):

        context = {

        }

        return render(request=self.request, template_name='gerenciar_servicos.html', context=context)


class GerenciarProdutos(View):
    def get(self, *args, **kwargs):
        context = {

        }

        return render(request=self.request, template_name='gerenciar_produtos.html', context=context)