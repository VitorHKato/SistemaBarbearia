# Generated by Django 3.2.5 on 2021-08-05 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210721_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='RendaMensal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anomes', models.CharField(max_length=20)),
                ('total_venda_produtos', models.FloatField(null=True)),
                ('total_servicos', models.FloatField(null=True)),
                ('total_comissoes', models.FloatField(null=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.RenameField(
            model_name='salariomensal',
            old_name='salario_total',
            new_name='comissao_total',
        ),
        migrations.RemoveField(
            model_name='salariomensal',
            name='data_pagamento',
        ),
        migrations.AddField(
            model_name='produto',
            name='preco',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='salariomensal',
            name='anomes',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='tarefasagendadas',
            name='cliente',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='tarefasagendadas',
            name='realizado',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('senha', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True)),
                ('funcionario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.funcionario')),
            ],
        ),
    ]
