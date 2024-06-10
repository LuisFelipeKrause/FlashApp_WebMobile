from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Revisar(LoginRequiredMixin, View):
    def get(self, request, pk):
        return render(request, 'revisar_app/revisao.html')
