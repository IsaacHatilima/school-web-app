from django.shortcuts import render
from django.views import View


class DashboardView(View):
    template_name = '_base.html'

    def get(self, request):
        return render(request, self.template_name)
