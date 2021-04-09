# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone

from django.db import models
import md5, datetime, time, json, math
from django.template.defaultfilters import slugify

from django.contrib import admin



class Category(models.Model):

    name = models.CharField(max_length=255, null=True, verbose_name="Nazwa kategorii")
    slug = models.SlugField(unique=True, editable=False, null=True)
    active = models.BooleanField(default=True, verbose_name="Aktywne")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"
        ordering = ['name']


    def save(self, *args, **kwargs):
		if self.slug == None:
			tmp = Category.objects.filter(slug=slugify(self.name)).count()
			if tmp == 0:
				tmp = ""
			self.slug = slugify(self.name + str(tmp))
		super(Category, self).save(*args, **kwargs)



class User(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Imię")
    surname = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nazwisko")
    nick = models.CharField(max_length=100, null=True, verbose_name="Nick")
    email = models.CharField(max_length=100, null=True, verbose_name="Email")
    password = models.CharField(max_length=100, null=True, verbose_name="Hasło")
    activate_acc = models.CharField(max_length=255, null=True, verbose_name="Aktywacja")
    active = models.BooleanField(default=False, verbose_name="Aktywne")
    creation_date = models.DateTimeField(editable=False, default=timezone.now, verbose_name="Data utworzenia")

    def __unicode__(self):
        return self.nick

    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"
        ordering = ['-creation_date']

    def save(self, *args, **kwargs):
        if self.activate_acc == None:
            self.activate_acc = md5.new(self.nick + str(time.time())).hexdigest()
            self.password = md5.new(self.password).hexdigest()
        super(User, self).save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=255, null=True, verbose_name="Tytuł")
    short = models.CharField(max_length=255, null=True, verbose_name="Krótki tekst")
    slug = models.SlugField(unique=True, editable=False, null=True)
    category = models.ForeignKey(Category, null=True, verbose_name="Kategoria")
    image = models.ImageField(upload_to="posts/", null=True, blank=True, verbose_name="Obrazek")
    text = models.TextField(null=True, blank=True, verbose_name="Treść HTML")
    creation_date = models.DateTimeField(editable=False, default=timezone.now, verbose_name="Data utworzenia")
    active = models.BooleanField(default=True, verbose_name="Aktywne")
    views = models.IntegerField(default=0, editable=False, verbose_name="Wyświetlenia")
    block = models.CharField(max_length=255, null=True, blank=True, verbose_name="Hasło blokady")


    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posty"
        ordering = ['title']

    def save(self, *args, **kwargs):
        if self.slug == None:
            tmp = Post.objects.filter(slug=slugify(self.title)).count()
            if tmp == 0:
                tmp = ""
            self.slug = slugify(self.title + str(tmp))

        super(Post, self).save(*args, **kwargs)



class Comment(models.Model):
    creation_date = models.DateTimeField(editable=False, default=timezone.now, verbose_name="Data utworzenia")
    comment = models.CharField(max_length=255, null=True, verbose_name="Komentarz")
    nick = models.CharField(max_length=255, null=True, verbose_name="Nick")
    ip = models.CharField(max_length=50, null=True, verbose_name="Adres IP")
    post = models.ForeignKey('Post', null=True, related_name='comment_post', verbose_name="Post")


    def __unicode__(self):
        return self.comment[:25]

    class Meta:
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"
        ordering = ['-creation_date']



class Photo(models.Model):
    image = models.ImageField(upload_to="photos/", null=True, blank=True, verbose_name="Obrazek")

    def __unicode__(self):
        return self.image.url

    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"
