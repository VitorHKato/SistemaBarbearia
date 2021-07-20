import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

import core.models


class Home(View):
    def get(self, *args, **kwargs):
        data_atual = datetime.datetime.now().date()

        lista_horarios = list(core.models.Horario.objects.filter(status=True).order_by('horario'))
        lista_tarefas_agendadas = list(core.models.TarefasAgendadas.objects.filter(status=True, data=data_atual).order_by('horario_inicio'))

        context = {
            'Titulo': "Bem vindo à Barber's!.",
            'lista_horarios': lista_horarios,
            'lista_tarefas_agendadas': lista_tarefas_agendadas,
        }

        return render(request=self.request, template_name='index.html', context=context)

class GerenciarFuncionarios(View):
    def get(self, *args, **kwargs):

        funcionarios = core.models.Funcionario.objects.filter(status=True)
        data_atual = datetime.datetime.now().date()

        lista_funcionarios = []
        for i in funcionarios:
            ultimo_salario = core.models.SalarioMensal.objects.filter(status=True, funcionario=i).last()
            dias = data_atual - i.dt_nascimento
            idade = dias.days / 365

            a = {
                'id': i.id,
                'nome_completo': i.nome + ' ' + i.sobrenome,
                'idade': int(idade),
                'situacao': i.situacao,
                'salario_fixo': i.salario_fixo,
                'cargo': i.cargo,
                'ultimo_salario': ultimo_salario.salario_total if ultimo_salario else '---',
            }
            lista_funcionarios.append(a)

        context = {
            'lista_funcionarios': lista_funcionarios,
        }

        return render(request=self.request, template_name='gerenciar_funcionarios.html', context=context)

class CriarFuncionario(View):
    def post(self, *args, **kwargs):
        nome = self.request.POST.get('nome')
        sobrenome = self.request.POST.get('sobrenome')
        dt_nascimento = self.request.POST.get('dt_nascimento')
        salario_fixo = self.request.POST.get('salario_fixo')
        cargo = self.request.POST.get('cargo')

        try:
            core.models.Funcionario.objects.create(
                nome=nome,
                sobrenome=sobrenome,
                dt_nascimento=dt_nascimento,
                salario_fixo=salario_fixo,
                cargo=cargo,
            ).save()

            msg = 'Funcionário criado com sucesso.'
        except:
            msg = 'Erro ao criar funcionário.'
        context = {
          'msg': msg,
        }

        return JsonResponse(context, safe=False)

class DeletarFuncionario(View):
    def post(self, *args, **kwargs):
        id_funcionario = self.request.POST.get('id_funcionario')

        funcionario = core.models.Funcionario.objects.filter(pk=id_funcionario).first()

        if funcionario:
            funcionario.delete()
            msg = 'Funcionário deletado.'
        else:
            msg = 'Funcionário não encontrado.'

        return JsonResponse(msg, safe=False)

class EditarFuncionario(View):
    def post(self, *args, **kwargs):
        id_funcionario = self.request.POST.get('id_funcionario')
        situacao = self.request.POST.get('situacao')
        salario_fixo = self.request.POST.get('salario_fixo')
        cargo = self.request.POST.get('cargo')

        filtros = {}

        if situacao:
            filtros['situacao'] = situacao
        if salario_fixo:
            filtros['salario_fixo'] = salario_fixo
        if cargo:
            filtros['cargo'] = cargo

        try:
            core.models.Funcionario.objects.filter(pk=id_funcionario).first().update(filtros)
            msg = 'Produto alterado com sucesso.'
        except Exception as e:
            msg = str(e)

        return JsonResponse(msg, safe=False)

class GerenciarServicos(View):
    def get(self, *args, **kwargs):

        lista_servicos = core.models.Servicos.objects.filter(status=True)

        context = {
            'lista_servicos': lista_servicos,
        }

        return render(request=self.request, template_name='gerenciar_servicos.html', context=context)

class CriarServico(View):
    def post(self, *args, **kwargs):
        nome = self.request.POST.get('nome')
        valor = self.request.POST.get('valor')
        comissao = self.request.POST.get('comissao')
        duracao = self.request.POST.get('duracao')

        try:
            core.models.Servicos.objects.create(
                nome=nome,
                valor=valor,
                comissao=comissao,
                duracao=duracao,
            ).save()

            msg = 'Serviço criado com sucesso.'
        except:
            msg = 'Erro ao criar serviço.'
        context = {
          'msg': msg,
        }

        return JsonResponse(context, safe=False)

class DeletarServico(View):
    def post(self, *args, **kwargs):
        id_servico = self.request.POST.get('id_servico')

        servico = core.models.Servicos.objects.filter(pk=id_servico).first()

        if servico:
            servico.delete()
            msg = 'Serviço deletado.'
        else:
            msg = 'Serviço não encontrado.'

        return JsonResponse(msg, safe=False)

class EditarServico(View):
    def post(self, *args, **kwargs):
        id_servico = self.request.POST.get('id_servico')
        nome = self.request.POST.get('nome')
        valor = self.request.POST.get('valor')
        comissao = self.request.POST.get('comissao')
        duracao = self.request.POST.get('duracao')

        filtros = {}

        if nome:
            filtros['nome'] = nome
        if valor:
            filtros['valor'] = valor
        if comissao:
            filtros['comissao'] = comissao
        if duracao:
            filtros['duracao'] = duracao

        try:
            core.models.Servicos.objects.filter(pk=id_servico).first().update(filtros)
            msg = 'Serviço alterado com sucesso.'
        except Exception as e:
            msg = str(e)

        return JsonResponse(msg, safe=False)

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