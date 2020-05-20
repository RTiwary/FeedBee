from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
@user_passes_test(lambda user: True if user.get_access('bulk_email') else False, login_url='/user/login')