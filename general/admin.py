# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import User, Category, Post, Comment, Photo
from django import forms
#from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    #text = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 20}), label="Treść HTML", required=False)

    class Meta:
        model = Post
        fields = "__all__"

class PostAdmin(admin.ModelAdmin):
    form = PostForm


admin.site.register(Category)
admin.site.register(User)
#admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(Post)
