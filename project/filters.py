# -*- coding: utf-8 -*-
#
# Author: Stanislav Glebov <glebofff@gmail.com> 
# Created: 17.07.16

from django.template.defaulttags import register


@register.filter
def get(dictionary, key):
    return dictionary.get(key)
