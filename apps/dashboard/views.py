from django.contrib.auth import get_user_model

from core.mixins import TemplateLoginRequiredMixin

User = get_user_model()


class IndexView(TemplateLoginRequiredMixin):
    template_name = 'administrator/index.html'

    def get(self, request, *args, **kwargs):
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UploadImagesView(TemplateLoginRequiredMixin):
    template_name = 'administrator/uploads/upload_image.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AssignUserView(TemplateLoginRequiredMixin):
    template_name = 'administrator/users/assign_user.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AssignBoatView(TemplateLoginRequiredMixin):
    template_name = 'administrator/users/assign_boat.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportTurtleView(TemplateLoginRequiredMixin):
    template_name = 'administrator/reports/report_turtle.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportClientView(TemplateLoginRequiredMixin):
    template_name = 'administrator/reports/report_client.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportGeneralView(TemplateLoginRequiredMixin):
    template_name = 'administrator/reports/report_general.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportRangeDateView(TemplateLoginRequiredMixin):
    template_name = 'administrator/reports/report_range_date.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
