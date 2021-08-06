from django.urls import path

from core.views import Home, GerenciarFuncionarios, GerenciarServicos, GerenciarProdutos, CriarProduto, DeletarProduto, \
    EditarProduto, CriarServico, EditarServico, DeletarServico, CriarFuncionario, DeletarFuncionario, EditarFuncionario, \
    ValidaNome, GerenciarTarefas, AgendarTarefa, Login, ValidarLogin

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('validar_login', ValidarLogin.as_view(), name='validar_login'),

    # path('valida_nome', ValidaNome.as_view(), name='valida_nome'),

    path('home', Home.as_view(), name='index'),

    path('gerenciar_produtos', GerenciarProdutos.as_view(), name='gerenciar_produtos'),
    path('criar_produto', CriarProduto.as_view(), name='criar_produto'),
    path('deletar_produto', DeletarProduto.as_view(), name='deletar_produto'),
    path('editar_produto', EditarProduto.as_view(), name='editar_produto'),

    path('gerenciar_servicos', GerenciarServicos.as_view(), name='gerenciar_servicos'),
    path('criar_servico', CriarServico.as_view(), name='criar_servico'),
    path('deletar_servico', DeletarServico.as_view(), name='deletar_servico'),
    path('editar_servico', EditarServico.as_view(), name='editar_servico'),

    path('gerenciar_funcionarios', GerenciarFuncionarios.as_view(), name='gerenciar_funcionarios'),
    path('criar_funcionario', CriarFuncionario.as_view(), name='criar_funcionario'),
    path('deletar_funcionario', DeletarFuncionario.as_view(), name='deletar_funcionario'),
    path('editar_funcionario', EditarFuncionario.as_view(), name='editar_funcionario'),

    path('gerenciar_tarefas', GerenciarTarefas.as_view(), name='gerenciar_tarefas'),
    path('agendar_tarefa', AgendarTarefa.as_view(), name='agendar_tarefa')

]