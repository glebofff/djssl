# -*- coding: utf-8 -*-
#
# Author: Stanislav Glebov <glebofff@gmail.com> 
# Created: 17.07.16

from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
