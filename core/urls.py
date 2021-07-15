from django.urls import path

from core.views import Home, GerenciarFuncionarios, GerenciarServicos, GerenciarProdutos

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('gerenciar_funcionarios', GerenciarFuncionarios.as_view(), name='gerenciar_funcionarios'),
    path('gerenciar_servicos', GerenciarServicos.as_view(), name='gerenciar_servicos'),
    path('gerenciar_funcionarios', GerenciarFuncionarios.as_view(), name='gerenciar_funcionarios'),
    path('gerenciar_produtos', GerenciarProdutos.as_view(), name='gerenciar_produtos'),
]