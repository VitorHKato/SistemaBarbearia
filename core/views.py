from django.shortcuts import render
from django.views import View


class Home(View):
    def get(self, *args, **kwargs):

        context = {
            'Titulo': "Bem vindo à Barber's!.",
        }

        return render(request=self.request, template_name='index.html', context=context)
