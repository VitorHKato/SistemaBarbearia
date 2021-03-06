from django.db import models
from django.db.models import DO_NOTHING

class Horario(models.Model):
    horario = models.CharField(max_length=50, null=True)
    status = models.BooleanField(default=True)

class Produto(models.Model):
    nome = models.CharField(max_length=100, null=True)
    quantidade = models.IntegerField(null=True)
    status = models.BooleanField(default=True)
    grupo = models.CharField(max_length=100, null=True)
    subgrupo = models.CharField(max_length=100, null=True)

class Servicos(models.Model):
    nome = models.CharField(max_length=200, null=True)
    valor = models.FloatField(null=True)
    comissao = models.IntegerField(null=True)
    status = models.BooleanField(default=True)
    duracao = models.CharField(max_length=50, null=True)

class Funcionario(models.Model):
    nome = models.CharField(max_length=100, null=True)
    sobrenome = models.CharField(max_length=100, null=True)
    dt_nascimento = models.DateField(null=True)
    situacao = models.CharField(max_length=100, null=True, default='TRABALHANDO')      #Se está de férias, afastado, etc
    salario_fixo = models.FloatField(null=True)
    status = models.BooleanField(default=True)
    cargo = models.CharField(max_length=100, null=True)

class SalarioMensal(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=DO_NOTHING)
    # comissao_total = models.FloatField(null=True)
    data_pagamento = models.DateField(null=True)
    salario_total = models.FloatField(null=True)
    status = models.BooleanField(default=True)

class TarefasAgendadas(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=DO_NOTHING)
    servico = models.ForeignKey(Servicos, on_delete=DO_NOTHING)
    horario_inicio = models.CharField(max_length=50, null=True)
    horario_fim = models.CharField(max_length=50, null=True)
    data = models.DateField(null=True)
    realizado = models.BooleanField(default=True)
    status = models.BooleanField(default=True)