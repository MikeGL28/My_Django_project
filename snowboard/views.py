from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from unicodedata import category
from django.utils import timezone

from .api_geo import apiKey
from .forms import PostForm
from .models import PostSnow
from .utils import geocode_address_yandex, reverse_geocode_yandex


from django.shortcuts import render, get_object_or_404
from .models import PostSnow

class PostSnowView(ListView):
    model = PostSnow
    template_name = 'snowboarding.html'
    context_object_name = 'posts'
    ordering = ['-published_at']


class PostCreateView(CreateView):
    model = PostSnow
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('snowboard:snowboarding')

    def form_valid(self, form):
        address = form.cleaned_data.get('address')
        if address:
            api_key = apiKey
            latitude, longitude = geocode_address_yandex(address, api_key)
            if latitude and longitude:
                form.instance.latitude = latitude
                form.instance.longitude = longitude
            else:
                print(f"Ошибка: Координаты не получены для адреса '{address}'.")
                return self.form_invalid(form)

        response = super().form_valid(form)
        return response
