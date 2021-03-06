# Generated by Django 3.2.5 on 2021-07-14 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, null=True)),
                ('sobrenome', models.CharField(max_length=100, null=True)),
                ('dt_nascimento', models.DateTimeField(null=True)),
                ('situacao', models.CharField(max_length=100, null=True)),
                ('salario_fixo', models.FloatField(null=True)),
                ('status', models.BooleanField(default=True)),
                ('cargo', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, null=True)),
                ('quantidade', models.IntegerField(null=True)),
                ('status', models.BooleanField(default=True)),
                ('grupo', models.CharField(max_length=100, null=True)),
                ('subgrupo', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Servicos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, null=True)),
                ('valor', models.FloatField(null=True)),
                ('comissao', models.IntegerField(null=True)),
                ('status', models.BooleanField(default=True)),
                ('duracao', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TarefasAgendadas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(null=True)),
                ('realizado', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.funcionario')),
                ('servico', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.servicos')),
            ],
        ),
        migrations.CreateModel(
            name='SalarioMensal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comissao_total', models.FloatField(null=True)),
                ('salario_total', models.FloatField(null=True)),
                ('status', models.BooleanField(default=True)),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.funcionario')),
            ],
        ),
    ]
