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

class DeletarProduto(View):
    def post(self, *args, **kwargs):
        id_produto = self.request.POST.get('id_produto')

        produto = core.models.Produto.objects.filter(pk=id_produto).first()

        if produto:
            produto.delete()
            msg = 'Produto deletado.'
        else:
            msg = 'Produto não encontrado.'

        return JsonResponse(msg, safe=False)

class EditarProduto(View):
    def post(self, *args, **kwargs):
        id_produto = self.request.POST.get('id_produto')
        nome = self.request.POST.get('nome')
        grupo = self.request.POST.get('grupo')
        quantidade = self.request.POST.get('quantidade')
        subgrupo = self.request.POST.get('subgrupo')

        filtros = {}

        if nome:
            filtros['nome'] = nome
        if grupo:
            filtros['grupo'] = grupo
        if quantidade:
            filtros['quantidade'] = quantidade
        if subgrupo:
            filtros['subgrupo'] = subgrupo

        try:
            core.models.Produto.objects.filter(pk=id_produto).first().update(filtros)
            msg = 'Produto alterado com sucesso.'
        except Exception as e:
            msg = str(e)

        return JsonResponse(msg, safe=False)