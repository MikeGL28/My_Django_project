from django.shortcuts import render
from .models import Certificate, TelegramPost

def programming_page(request):
    certificates = Certificate.objects.all().order_by('-created_at')
    telegram_posts = TelegramPost.objects.all().order_by('-created_at').reverse()[:10]  # последние 5 постов
    resume_url = "/media/resume/Mikhail_Gavrilov_resume.pdf"
    return render(request, 'index.html', {
        'certificates': certificates,
        'telegram_posts': telegram_posts,
        'resume_url': resume_url
    })
