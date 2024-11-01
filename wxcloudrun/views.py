import logging
from django.shortcuts import render

logger = logging.getLogger('log')

def index(request):
    return render(request, 'index.html')