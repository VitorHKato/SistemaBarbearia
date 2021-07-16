from django.urls import path

from core.views import Home, GerenciarFuncionarios, GerenciarServicos, GerenciarProdutos, CriarProduto, DeletarProduto, \
    EditarProduto

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('gerenciar_funcionarios', GerenciarFuncionarios.as_view(), name='gerenciar_funcionarios'),
    path('gerenciar_servicos', GerenciarServicos.as_view(), name='gerenciar_servicos'),
    path('gerenciar_funcionarios', GerenciarFuncionarios.as_view(), name='gerenciar_funcionarios'),

    path('gerenciar_produtos', GerenciarProdutos.as_view(), name='gerenciar_produtos'),
    path('criar_produto', CriarProduto.as_view(), name='criar_produto'),
    path('deletar_produto', DeletarProduto.as_view(), name='deletar_produto'),
    path('editar_produto', EditarProduto.as_view(), name='editar_produto'),
]