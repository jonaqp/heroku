from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView

from apps.customer.models import UserProfile


class TemplateLoginRequiredMixin(LoginRequiredMixin, TemplateView):
    login_url = '/'

    def __init__(self, **kwargs):
        self.modules = None
        self.current_user = None
        super().__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/?next=%s' % request.path)

        if not cache.get('modules'):
            self.modules = request.user.get_menu()
            cache.set('modules', self.modules, 30 * 60)
        else:
            self.modules = cache.get('modules')
        self.current_user = UserProfile.objects.get(
            user__email=request.user.email)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.modules
        context['request_path'] = self.request.get_full_path()
        context['current_user'] = self.current_user
        return context


class ListViewRequiredMixin(LoginRequiredMixin, ListView):
    pass
