# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from models import Category, User, Post, Comment, Photo
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.mail import send_mail


def index(request):
    context = {}
    context['posts'] = Post.objects.all()
    return render(request, 'index.html', context)


@csrf_exempt
def report(request):
    context = {}
    added = ''
    if request.method == 'POST':
        subject = request.POST.get("subject")
        content = request.POST.get("content")
        send_mail(
            subject,
            content,
            'kontakt@mrokas.usermd.net',
            ['patryk.mroczkowski@gmail.com'],
            fail_silently=True,
        )
        added = 'Pomyślnie wysłano wiadomość'

    context['added'] = added
    return render(request, 'report.html', context)


@csrf_exempt
def post(request, post_slug):
    context = {}

    post = Post.objects.filter(slug = post_slug).first()
    added = ''

    if request.method == 'POST':
        comment = Comment(comment=request.POST.get("comment"), nick=request.POST.get("nick"), ip=get_client_ip(request), post = post)
        comment.save()
        added = 'Pomyślnie dodano komentarz'

    context['added'] = added
    context['post'] = post
    context['comments'] = Comment.objects.filter(post=post)
    return render(request, 'post.html', context)


def category(request, category_slug):
    context = {}
    category = Category.objects.filter(slug=category_slug).first()
    context['posts'] = Post.objects.filter(category=category)
    context['category'] = category
    return render(request, 'categories.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
