# -*- coding: utf-8 -*-
#
# Author: Stanislav Glebov <glebofff@gmail.com> 
# Created: 17.07.16
from django.shortcuts import render, redirect
from django.db.models import ObjectDoesNotExist
from forms import UploadFileForm
from certs.models import Cert
from OpenSSL import crypto
import logging
logger = logging.getLogger(__name__)


def index(request):
    form = UploadFileForm()

    return render(request, 'index.html', {
        'form': form,
        'count': Cert.objects.count()
    })


def upload(request):
    if request.method != 'POST':
        return redirect('index')

    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        f = request.FILES['file']
        try:
            name = str(f)
            try:
                isnew = False
                c = Cert.objects.get(filename=name)
            except ObjectDoesNotExist:
                isnew = True
                c = Cert()

            c.frombuffer(f.read())
            if isnew:
                c.filename = name
            c.save()

            return render(request, 'success.html', {
                'vdict': c.verbose_dict(),
                'cert': c,
                'isnew': isnew
            })
        except crypto.Error as e:
            raise e

    return redirect('index')
