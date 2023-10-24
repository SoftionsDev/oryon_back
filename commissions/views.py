from django.shortcuts import render
from django.http import JsonResponse
from .models import Commission

def get_commissions(request):
    commissions = Commission.objects.all()
    data = {
        'commissions': list(commissions.values())
    }
    return JsonResponse(data)
