# -*- coding: utf-8 -*-
from django import template
import datetime
from general.models import Category
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def categories(context):

    request = context['request']
    categories = Category.objects.filter(active=True)
    return_all = ""
    for category in categories:
        return_all += '<a href="/kategoria/' + category.slug + '"><li>' + category.name + '</li></a>'

    return mark_safe(return_all)
