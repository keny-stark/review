from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.urls.base import reverse_lazy, reverse
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from webapp.forms import ReviewForm
from webapp.models import Product, Review


class ReviewView(ListView):
    context_object_name = 'review'
    model = Review
    template_name = 'review/review_all_view.html'


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review/review_detail_view.html'


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_add.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        project = Review.objects.get(pk=self.kwargs['pk'])
        users = project.users.all()
        if self.request.user in users:
            return True
        return False

    def get_success_url(self):
        return reverse('webapp:review_detail', kwargs={'pk': self.object.pk})


class ReviewUpdate(PermissionRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_edit.html'
    permission_required = 'webapp.update_review'
    permission_denied_message = 'poshel von'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author or self.request.user.is_superuser

    def get_success_url(self):
        return reverse('webapp:review_detail', kwargs={'pk': self.object.pk})


class DeleteReview(PermissionRequiredMixin, DeleteView):
    template_name = 'review/review_delete.html'
    model = Review
    context_object_name = 'review'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.update_review'
    permission_denied_message = 'poshel von'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author or self.request.user.is_superuser

    def get_success_url(self):
        return reverse('accounts:login')

