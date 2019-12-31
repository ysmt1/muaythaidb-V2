from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Count, Avg, Sum, F
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from .models import Gym, Review, GymImage, ReviewImage, Like
from .forms import ReviewCreateForm, ReviewFormSet

def index(request):
    gyms = Gym.objects.annotate(count = Count('review'), avg = Avg('review__rating_overall'), total_days = Sum('review__training_length'))
    top_rated = gyms.exclude(review=None).order_by('-avg')[0].name
    most_reviewed = gyms.exclude(review=None).order_by('-count')[0].name
    total_review_count = gyms.aggregate(total_reviews = Sum('count'))
    latest_review = Review.objects.order_by('-date_created')[0]
    context = {
        'gyms': gyms,
        'top_rated': top_rated,
        'most_reviewed': most_reviewed,
        'total_review_count': total_review_count['total_reviews'],
        'latest_review': latest_review
    }
    return render(request, 'mtdb/index.html', context)

class GymDetailView(DetailView):
    model = Gym
    
    def get_object(self):
        return get_object_or_404(Gym, name = self.kwargs['gym_name'].replace("_", " "))

    def get_context_data(self, *args, **kwargs):
        context = super(GymDetailView, self).get_context_data(*args, **kwargs)
        context['reviews'] = Review.objects.filter(gym = self.object.id).annotate(like_count = Count('like__liked')).order_by('-date_created')
        context['gym_images'] = GymImage.objects.filter(gym = self.object.id)
        return context

class ReviewCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name_suffix = '_create_form'
    success_message = 'Review Successfully Posted!'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(ReviewCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = ReviewCreateForm(self.request.POST)
            context['formset'] = ReviewFormSet(self.request.POST, self.request.FILES)
        else:
            context['form'] = ReviewCreateForm()
            context['formset'] = ReviewFormSet()
        return context       

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['form']
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            form.instance.author = self.request.user
            self.object = form.save()
            form.instance = self.object
            form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ReviewUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewCreateForm
    template_name_suffix = '_create_form'
    success_message = 'Review Updated!'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(ReviewUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = ReviewCreateForm(self.request.POST, instance=self.object)
            context['formset'] = ReviewFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['form'] = ReviewCreateForm(instance=self.object)
            context['formset'] = ReviewFormSet(instance=self.object)
        return context       

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['form']
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            form.instance.author = self.request.user
            self.object = form.save()
            form.instance = self.object
            form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_message = 'Deleted Review!'
    success_url = reverse_lazy('index')

    def test_func(self):
        if self.request.user.id == self.get_object().author.id:
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
            messages.success(self.request, self.success_message)
            return super(ReviewDeleteView, self).delete(request, *args, **kwargs)

@require_http_methods(["POST"])
def like_view(request, review_id, route):
    error = None
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'Please Login'})
    review = get_object_or_404(Review, id=review_id)
    if Like.objects.filter(user=user, review=review).exists():
        if route == 'unlike':
            instance = Like.objects.get(user=user, review=review)
            instance.delete()
            like_count = Like.objects.filter(review=review).count()
        else:
            error = 'You have already liked this review!'
    else:
        if route == 'unlike':
            error = 'You have not liked this review!'
        else:
            like = Like(user=user, review=review, liked=True)
            like.save()
            like_count = Like.objects.filter(review=review).count()

    if error is None:
        return JsonResponse({'success': like_count})
    else:
        return JsonResponse({'error': error})

    