from json import loads

from django.contrib import messages
from django.contrib.auth import get_user_model

from core import constants as core_constants
from core.mixins import TemplateLoginRequiredMixin
from .forms import ContainerForm, TripForm
from .models import Container, Trip

User = get_user_model()


class ViewerBoatView(TemplateLoginRequiredMixin):
    template_name = 'container/viewer/index.html'

    def get(self, request, *args, **kwargs):
        self.boats = Container.objects.all().values_list('identifier_mac', flat=True)
        print(self.boats)
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boats'] = self.boats
        return context


class EditorBoatView(TemplateLoginRequiredMixin):
    template_name = 'container/editor/index.html'

    def get(self, request, *args, **kwargs):
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContainerView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/container/container.html'

    def __init__(self, **kwargs):
        self.form_container = None
        self.container_all = None
        super().__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.container_all = Container.objects.all()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.form_container = ContainerForm(auto_id='id_container_%s')
        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.form_container = ContainerForm(
            data=request.POST, auto_id='id_container_%s')
        if self.form_container.is_valid():
            self.form_container.save()
            messages.success(request, core_constants.MESSAGE_TAGS['success'])
        else:
            messages.warning(request, core_constants.MESSAGE_TAGS['warning'])

        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_container'] = self.form_container
        context['list_containers'] = self.container_all
        return context


class ContainerEditView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/container/container_add.html'

    def __init__(self, **kwargs):
        self.form_container = None
        self.container = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        container = request.GET['container_id']
        self.container = Container.objects.get(pk=container)
        self.form_container = ContainerForm(
            auto_id='id_container_%s', instance=self.container)
        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        data = loads(request.body.decode('utf-8'))
        data_container_pk = data['form_pk']
        data_form_container = data['form']
        self.container = Container.objects.get(pk=data_container_pk)
        self.form_container = ContainerForm(
            data_form_container, auto_id='id_container_%s', instance=self.container)

        if self.form_container.is_valid():
            self.form_container.save()

            messages.success(request, core_constants.MESSAGE_TAGS['success'])
        else:
            messages.error(request, core_constants.MESSAGE_TAGS['error'])
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_container'] = self.form_container
        context['form_pk'] = self.container.id
        context['btn_edit'] = core_constants.BTN_EDIT
        return context


class ContainerListView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/container/container_list.html'

    def __init__(self, **kwargs):
        self.container_all = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        self.container_all = Container.objects.all()
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_containers'] = self.container_all
        return context


class TripView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/container/trip.html'

    def __init__(self, **kwargs):
        self.form_trip = None
        self.trip_all = None
        super().__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.trip_all = Trip.objects.all()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.form_trip = TripForm(auto_id='id_trip_%s')
        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.form_trip = TripForm(
            data=request.POST, auto_id='id_trip_%s')
        if self.form_trip.is_valid():
            self.form_trip.save()
            messages.success(request, core_constants.MESSAGE_TAGS['success'])
        else:
            messages.warning(request, core_constants.MESSAGE_TAGS['warning'])

        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_trip'] = self.form_trip
        context['list_trips'] = self.trip_all
        return context


class TripEditView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/container/trip_add.html'

    def __init__(self, **kwargs):
        self.form_trip = None
        self.trip = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        trip = request.GET['trip_id']
        self.trip = Trip.objects.get(pk=trip)
        self.form_trip = TripForm(
            auto_id='id_trip_%s', instance=self.trip)
        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        data = loads(request.body.decode('utf-8'))
        data_trip_pk = data['form_pk']
        data_form_trip = data['form']
        self.trip = Trip.objects.get(pk=data_trip_pk)
        self.form_trip = TripForm(
            data_form_trip, auto_id='id_trip_%s', instance=self.trip)
        if self.form_trip.is_valid():
            self.form_trip.save()
            messages.success(request, core_constants.MESSAGE_TAGS['success'])
        else:
            messages.error(request, core_constants.MESSAGE_TAGS['error'])
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_trip'] = self.form_trip
        context['form_pk'] = self.trip.id
        context['btn_edit'] = core_constants.BTN_EDIT
        return context


class TripListView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/container/trip_list.html'

    def __init__(self, **kwargs):
        self.trip_all = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        self.trip_all = Trip.objects.all()
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_trips'] = self.trip_all
        return context
