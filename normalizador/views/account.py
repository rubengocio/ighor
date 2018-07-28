# -*- coding: utf-8 -*-
from django.shortcuts import redirect


def redirect_account(request):
    return redirect('/admin/login?next=/')