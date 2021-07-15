from django.http import JsonResponse
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

        lista_produtos = list(core.models.Produto.objects.filter(status=True))

        context = {
            'lista_produtos': lista_produtos,
        }

        return render(request=self.request, template_name='gerenciar_produtos.html', context=context)

class CriarProduto(View):
    def post(self, *args, **kwargs):
        nome = self.request.POST.get('nome')
        quantidade = self.request.POST.get('quantidade')
        grupo = self.request.POST.get('grupo')
        subgrupo = self.request.POST.get('subgrupo')

        try:
            core.models.Produto.objects.create(
                nome=nome,
                quantidade=quantidade,
                grupo=grupo,
                subgrupo=subgrupo,
            ).save()

            msg = 'Produto criado com sucesso.'
        except:
            msg = 'Erro ao criar produto.'
        context = {
          'msg': msg,
        }

        return JsonResponse(context, safe=False)