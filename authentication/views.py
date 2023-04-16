from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect


class LoginView(View):
    template_name = 'auth/index.html'

    def get(self, request):
        return render(request, self.template_name)
        # if request.user.is_authenticated:
        #     if request.user.role == 'System Admin':
        #         return HttpResponseRedirect(reverse('admin_home'))
        # else:
        #     return render(request, self.template_name)
