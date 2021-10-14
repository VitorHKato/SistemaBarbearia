import datetime

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

import core.models

class Login(View):
    def get(self, *args, **kwargs):

        return render(request=self.request, template_name='login.html')

class ValidarLogin(View):
    def criptografar_senha(self, senha=None, *args, **kwargs):
        nova_senha = ''

        if senha:
            for i in senha:
                novo_char = ord(i) + 5
                nova_senha += str(chr(novo_char))

        return nova_senha

    def descriptografar_senha(self, senha=None, *args, **kwargs):
        senha_original = ''

        if senha:
            for i in senha:
                char = ord(i) - 5
                senha_original += str(chr(char))

        return senha_original

    def post(self, *args, **kwargs):
        usuario = self.request.POST.get('usuario')
        senha = self.request.POST.get('senha')

        # nova_senha = self.criptografar_senha(senha=senha)
        # senha_original = self.descriptografar_senha(senha=nova_senha)

        senha_criptografada = self.criptografar_senha(senha=senha)

        if core.models.Usuario.objects.filter(usuario=usuario, senha=senha_criptografada).exists():
            return redirect('index')
        else:
            return JsonResponse({'msg': 'Usuario invalido.'}, safe=False)

class ValidaNome(View):
    def get(self, *args, **kwargs):
        nome = self.request.GET.get('nome')

        context = {
            'nome': 'Nome enviado: ' + nome,
        }

        return JsonResponse(context)

class Home(View):
    def get(self, *args, **kwargs):
        data_atual = datetime.datetime.now().date()

        tarefas_agendadas = list(core.models.TarefasAgendadas.objects.filter(status=True, data=data_atual).order_by('horario_inicio'))

        lista_tarefas_agendadas = []
        for i in tarefas_agendadas:
            a = {
                'id': i.id,
                'funcionario_nome': i.funcionario.nome if i.funcionario and i.funcionario.nome else '---',
                'cliente_nome': i.cliente if i.cliente else '---',
                'servico_nome': i.servico.nome if i.servico and i.servico.nome else '---',
                'horario_inicio': i.horario_inicio + 'h' if i.horario_inicio else '---',
                'horario_fim': i.horario_fim + 'h' if i.horario_fim else '---',
                'data': i.data if i.data else '---',
                'realizado': 'Sim' if i.realizado else 'Não',
                'realizado_checkbox': i.realizado,
            }
            lista_tarefas_agendadas.append(a)

        context = {
            'Titulo': "Barbearia do Jow",
            'lista_tarefas_agendadas': lista_tarefas_agendadas,
            'true': True,
        }

        return render(request=self.request, template_name='index.html', context=context)

class GerenciarFuncionarios(View):
    def get(self, *args, **kwargs):
        funcionarios = core.models.Funcionario.objects.filter(status=True).order_by('pk')
        data_atual = datetime.datetime.now().date()

        data_string = str(data_atual).split('-')
        anomes = data_string[0] + data_string[1]

        #Salários pagos referente ao mês anterior
        salarios_mensais = list(core.models.SalarioMensal.objects.filter(status=True, anomes=anomes).order_by('funcionario__id'))

        lista_funcionarios = []
        for i in funcionarios:
            #ultimo_salario = core.models.SalarioMensal.objects.filter(status=True, funcionario=i).last()
            dias = data_atual - i.dt_nascimento if i.dt_nascimento else 0
            idade = dias.days / 365 if isinstance(dias, datetime.timedelta) else 0

            nome_completo = '---'
            if i.nome and i.sobrenome:
                nome_completo = i.nome + ' ' + i.sobrenome
            elif i.nome and not i.sobrenome:
                nome_completo = i.nome

            a = {
                'id': i.id,
                'nome_completo': nome_completo,
                'idade': int(idade),
                'situacao': i.situacao if i.situacao else '---',
                'salario_fixo': 'R$ ' + str(i.salario_fixo) if i.salario_fixo else '---',
                'cargo': i.cargo if i.cargo else '---',
                #'ultimo_salario': 'R$ ' + str(ultimo_salario.salario_total) if ultimo_salario else '---',
            }
            lista_funcionarios.append(a)

        lista_salarios_mensais = []
        for i in salarios_mensais:
            nome_completo = '---'
            if i.funcionario and i.funcionario.nome and i.funcionario.sobrenome:
                nome_completo = i.funcionario.nome + ' ' + i.funcionario.sobrenome
            elif i.funcionario.nome and not i.funcionario.sobrenome:
                nome_completo = i.funcionario.nome

            a = {
                'id': i.id,
                'nome_completo': nome_completo,
                'data_pagamento': data_string[1] + '/' + data_string[0],
                'salario_total': 'R$ ' + str(i.comissao_total) if i.comissao_total else '---',
            }
            lista_salarios_mensais.append(a)

        situacoes = ['TRABALHANDO', 'FÉRIAS', 'AFASTADO', 'LICENÇA']

        context = {
            'lista_funcionarios': lista_funcionarios,
            'lista_salarios_mensais': lista_salarios_mensais,
            'situacoes': situacoes,
        }

        return render(request=self.request, template_name='gerenciar_funcionarios.html', context=context)

class CriarFuncionario(View):
    def post(self, *args, **kwargs):
        nome = self.request.POST.get('nome')
        sobrenome = self.request.POST.get('sobrenome')
        dt_nascimento = self.request.POST.get('dt_nascimento')
        salario_fixo = self.request.POST.get('salario_fixo')
        situacao = self.request.POST.get('situacao')
        cargo = self.request.POST.get('cargo')

        data = dt_nascimento.split('/')

        try:
            data_nascimento = datetime.date(year=int(data[2]), month=int(data[1]), day=int(data[0]))
        except:
            data_nascimento = None

        try:
            core.models.Funcionario.objects.create(
                nome=nome,
                sobrenome=sobrenome,
                dt_nascimento=data_nascimento,
                situacao=situacao,
                salario_fixo=salario_fixo if salario_fixo is not '' else 0,
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
            core.models.Funcionario.objects.filter(pk=id_funcionario).update(**filtros)
            msg = 'Produto alterado com sucesso.'
        except Exception as e:
            msg = str(e)

        return JsonResponse(msg, safe=False)

class ViewEditarFuncionario(View):
    def get(self, *args, **kwargs):
        id_produto = self.kwargs['id_produto']

        funcionario = core.models.Funcionario.objects.filter(pk=id_produto).first()

        situacoes = ['TRABALHANDO', 'FÉRIAS', 'AFASTADO', 'LICENÇA']

        try:
            dt_nascimento = str(funcionario.dt_nascimento).split('-')
            dt_nascimento_formatada = dt_nascimento[0] + '-' + dt_nascimento[1] + '-' + dt_nascimento[2]
        except:
            dt_nascimento_formatada = None

        context = {
            'funcionario': funcionario,
            'situacoes': situacoes,
            'dt_nascimento': dt_nascimento_formatada,
        }

        return render(request=self.request, template_name='editar_funcionario.html', context=context)

class GerenciarServicos(View):
    def get(self, *args, **kwargs):

        servicos = core.models.Servicos.objects.filter(status=True).order_by('pk')

        lista_servicos = []
        for i in servicos:
            a = {
                'id': i.id,
                'nome': i.nome if i.nome else '---',
                'valor': 'R$ ' + str(i.valor) if i.valor else '---',
                'comissao': str(i.comissao) + '%' if i.comissao else '---',
                'duracao': i.duracao + 'h' if i.duracao else '---',
            }
            lista_servicos.append(a)

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
            core.models.Servicos.objects.filter(pk=id_servico).update(**filtros)
            msg = 'Serviço alterado com sucesso.'
        except Exception as e:
            msg = str(e)

        return JsonResponse(msg, safe=False)

class ViewEditarServico(View):
    def get(self, *args, **kwargs):
        id_servico = self.kwargs['id_servico']

        servico = core.models.Servicos.objects.filter(pk=id_servico).first()

        context = {
            'servico': servico,
        }

        return render(request=self.request, template_name='editar_servico.html', context=context)

class GerenciarProdutos(View):
    def get(self, *args, **kwargs):

        produtos = list(core.models.Produto.objects.filter(status=True).order_by('pk'))

        lista_produtos = []
        for i in produtos:
            a = {
                'id': i.id,
                'nome': i.nome if i.nome else '---',
                'quantidade': i.quantidade if i.quantidade else 0,
                'grupo': i.grupo if i.grupo else '---',
                'subgrupo': i.subgrupo if i.subgrupo else '---',
                'preco': 'R$ ' + str(i.preco) if i.preco else '---',
            }
            lista_produtos.append(a)

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
        preco = self.request.POST.get('preco')

        try:
            core.models.Produto.objects.create(
                nome=nome,
                quantidade=quantidade,
                grupo=grupo,
                subgrupo=subgrupo,
                preco=preco,
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
        preco = self.request.POST.get('preco')

        filtros = {}

        if nome:
            filtros['nome'] = nome
        if grupo:
            filtros['grupo'] = grupo
        if quantidade:
            filtros['quantidade'] = quantidade
        if subgrupo:
            filtros['subgrupo'] = subgrupo
        if preco:
            filtros['preco'] = preco

        try:
            core.models.Produto.objects.filter(pk=id_produto).update(**filtros)
            msg = 'Produto alterado com sucesso.'
        except Exception as e:
            msg = str(e)

        return JsonResponse(msg, safe=False)

class ViewEditarProduto(View):
    def get(self, *args, **kwargs):
        id_produto = self.kwargs['id_produto']

        produto = core.models.Produto.objects.filter(pk=id_produto).first()

        context = {
            'produto': produto,
        }

        return render(request=self.request, template_name='editar_produto.html', context=context)

class RemoverQuantidadeProduto(View):
    def post(self, *args, **kwargs):
        id_produto = self.request.POST.get('id_produto')

        produto = core.models.Produto.objects.filter(pk=id_produto).first()
        if produto:
            if produto.quantidade > 0:
                produto.quantidade = produto.quantidade - 1
                produto.save()
                msg = 'Removido um produto.'
            else:
                msg = 'Não há produtos em estoque.'
        else:
            msg = 'Não foi possível encontrar o produto.'

        return JsonResponse(msg, safe=False)

class AdicionarQuantidadeProduto(View):
    def post(self, *args, **kwargs):
        id_produto = self.request.POST.get('id_produto')

        produto = core.models.Produto.objects.filter(pk=id_produto).first()
        if produto:
            produto.quantidade = produto.quantidade + 1
            produto.save()
            msg = 'Adicionado um produto.'
        else:
            msg = 'Não foi possível encontrar o produto.'

        return JsonResponse(msg, safe=False)

class GerenciarTarefas(View):
    def get(self, *args, **kwargs):

        lista_servicos = list(core.models.Servicos.objects.filter(status=True).values('id', 'nome'))

        funcionarios = core.models.Funcionario.objects.filter(status=True, situacao='TRABALHANDO')

        lista_horarios = list(core.models.Horario.objects.filter(status=True).order_by('horario'))

        lista_funcionarios = []
        for i in funcionarios:
            nome_completo = '---'
            if i.nome and i.sobrenome:
                nome_completo = i.nome + ' ' + i.sobrenome
            elif i.nome and not i.sobrenome:
                nome_completo = i.nome
            nome_completo = nome_completo + ' (' + i.cargo + ')'
            a = {
                'id': i.id,
                'nome_completo': nome_completo,
            }
            lista_funcionarios.append(a)

        context = {
            'lista_servicos': lista_servicos,
            'lista_funcionarios': lista_funcionarios,
            'lista_horarios': lista_horarios,
        }

        return render(request=self.request, template_name='gerenciar_tarefas.html', context=context)

class AgendarTarefa(View):
    def post(self, *args, **kwargs):
        id_funcionario = self.request.POST.get('id_funcionario')
        id_servico = self.request.POST.get('id_servico')
        #TODO: Ver pq a data chega errada
        data_tarefa = self.request.POST.get('dataTarefa')
        hora_inicio = self.request.POST.get('horaInicio')
        hora_fim = self.request.POST.get('horaFim')
        nome_cliente = self.request.POST.get('nome_cliente')

        funcionario = core.models.Funcionario.objects.filter(id=id_funcionario).first()
        servico = core.models.Servicos.objects.filter(id=id_servico).first()

        data = data_tarefa.split('/')

        try:
            data_tarefa = datetime.date(year=int(data[2]), month=int(data[1]), day=int(data[0]))
        except:
            data_tarefa = None

        try:
            core.models.TarefasAgendadas.objects.create(
                funcionario=funcionario,
                servico=servico,
                horario_inicio=hora_inicio,
                horario_fim=hora_fim,
                data=data_tarefa,
                cliente=nome_cliente,
            ).save()

            msg = 'Tarefa agendada criada com sucesso!'
        except Exception as e:
            msg = 'Erro ao criar tarefa agendada.'

        context = {
            'msg': msg
        }

        return JsonResponse(context, safe=False)

class AvaliarTarefa(View):
    def post(self, *args, **kwargs):
        id_tarefa = self.request.POST.get('id_tarefa')
        avaliacao = self.request.POST.get('avaliacao')

        tarefa = core.models.TarefasAgendadas.objects.filter(pk=id_tarefa).first()

        if tarefa:
            if avaliacao == 'true':
                tarefa.realizado = True
            else:
                tarefa.realizado = False
            tarefa.save()

            msg = 'Tarefa avaliada com sucesso.'
        else:
            msg = 'Tarefa não encontrada.'

        return JsonResponse(msg, safe=False)

#TODO: Ao agendar tarefa, colocar na função para incrementar a comissao do funcionário e da renda mensal