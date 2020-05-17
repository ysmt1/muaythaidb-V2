from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Avg, Sum, F
from .models import Gym, Review, GymImage, ReviewImage, Like
from .forms import ReviewCreateForm, ReviewFormSet, ContactForm, AddGymForm

def index(request):
    gyms = Gym.objects.annotate(count = Count('review'), avg = Avg('review__rating_overall'), total_days = Sum('review__training_length'))
    top_rated = gyms.exclude(review=None).order_by('-avg')[0].name
    most_reviewed = gyms.exclude(review=None).order_by('-count')[0].name
    total_review_count = gyms.aggregate(total_reviews = Sum('count'))
    latest_review = Review.objects.order_by('-date_created')[0]
    gym_form = AddGymForm()
    context = {
        'gyms': gyms,
        'top_rated': top_rated,
        'most_reviewed': most_reviewed,
        'total_review_count': total_review_count['total_reviews'],
        'latest_review': latest_review,
        'form': gym_form
    }
    return render(request, 'mtdb/index.html', context)

def about(request):
    return render(request, 'mtdb/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = f"MTDB, message from {email} ({name})"

            send_mail(subject, message, "", ['yosuke.seki@gmail.com'])
            messages.success(request, 'Message Sent! Will Reply Shortly')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ContactForm()

    return render(request, 'mtdb/contact.html', {'form':form})

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
            context['form'] = ReviewCreateForm(self.request.POST, label_suffix="")
            context['formset'] = ReviewFormSet(self.request.POST, self.request.FILES)
        else:
            context['form'] = ReviewCreateForm(label_suffix="")
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

    def get_success_url(self):
        return self.object.gym.get_absolute_url()

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_message = 'Deleted Review!'

    def test_func(self):
        if self.request.user.id == self.get_object().author.id:
            return True
        else:
            return False

    def get_success_url(self):
        if self.request.POST.get('profile-delete'):
            return reverse('users:profile')
        else:
            return reverse('index')

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

@require_http_methods(["POST"])
def add_gym(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'Please Login'})

    if request.is_ajax() and request.method == 'POST':
        form = AddGymForm(request.POST)

        if form.is_valid():
            gym_name = form.cleaned_data['gym_name']
            gym_location = form.cleaned_data['gym_location']
            subject = f"MTDB, Add Gym {gym_name} in {gym_location}"

            send_mail(subject, subject, "", ['yosuke.seki@gmail.com'])
            return JsonResponse({'success': 'Request Sent!'})
        else:
            JsonResponse({'error': 'An Error as Occured!'})
    else:
        return JsonResponse({'error': 'An Error as Occured!'})
    