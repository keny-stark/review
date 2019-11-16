from abc import ABC
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls.base import reverse_lazy
from django.core.paginator import Paginator
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from webapp.forms import ReviewForm, ProductForm
from webapp.models import Product
from django.urls import reverse
from django.core.exceptions import PermissionDenied


class IndexView(ListView):
    context_object_name = 'product'
    model = Product
    template_name = 'product/product_view.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail_view.html'
    context_object_name = 'product'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'product/product_create.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('projects')
    permission_required = 'webapp.add_product'
    permission_denied_message = 'poshel von'

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_update.html'
    permission_required = 'webapp.update_product'
    permission_denied_message = 'poshel von'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'product/product_delete.html'
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_product'
    permission_denied_message = 'poshel von'
