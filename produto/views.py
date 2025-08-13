from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from perfil.models import Perfil

from . import models


# Create your views here.
class ListaProdutos(ListView):
    model = models.Produto
    template_name = "produto/lista.html"
    context_object_name = "produtos"
    paginate_by = 10


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = "produto/detalhe.html"
    context_object_name = "produto"
    slug_url_kwarg = "slug"


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AdicionarCarrinho')


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoverDoCarrinho')


class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')


class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')
