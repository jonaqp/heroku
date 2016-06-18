from json import loads

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction, IntegrityError

from apps.customer.models import GroupState
from apps.menu.forms import GroupForm, GroupModuleForm
from apps.menu.formset import GroupSubmoduleFormSet
from apps.menu.models import GroupModule, SubModule, GroupSubModule
from core import constants as core_constants
from core.mixins import TemplateLoginRequiredMixin, ListViewRequiredMixin

User = get_user_model()


class GroupView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/groups/group.html'

    def __init__(self, **kwargs):
        self.form_group = None
        self.group_all = None
        super().__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.group_all = GroupState.current.all().prefetch_related('group')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.form_group = GroupForm(auto_id='id_group_%s')
        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.form_group = GroupForm(request.POST, auto_id='id_group_%s')
        if self.form_group.is_valid():
            self.form_group.save()
            messages.success(request, core_constants.MESSAGE_TAGS['success'])
        else:
            messages.warning(request, core_constants.MESSAGE_TAGS['warning'])
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_group'] = self.form_group
        context['list_group'] = self.group_all
        return context


class GroupEditView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/groups/group_add.html'

    def __init__(self, **kwargs):
        self.form_group = None
        self.group = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        group = request.GET['group_id']
        self.group = Group.objects.get(pk=group)
        self.form_group = GroupForm(auto_id='id_group_%s',
                                    instance=self.group)
        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        data = loads(request.body.decode('utf-8'))
        data_group_pk = data['form_pk']
        data_form_group = data['form']
        self.group = Group.objects.get(pk=data_group_pk)
        self.form_group = GroupForm(
            data_form_group, auto_id='id_group_%s', instance=self.group)
        if self.form_group.is_valid():
            self.form_group.save(commit=False)
            self.form_group = GroupForm(auto_id='id_group_%s')
            messages.success(request, core_constants.MESSAGE_TAGS['success'])
        else:
            messages.error(request, core_constants.MESSAGE_TAGS['error'])
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_group'] = self.form_group
        context['form_pk'] = self.group.id
        context['btn_edit'] = core_constants.BTN_EDIT
        return context


class GroupListView(ListViewRequiredMixin):
    template_name = 'administrator/maintenance/groups/group_list.html'
    model = GroupState
    queryset = GroupState.current.all().iterator()
    context_object_name = 'list_group'


class GroupModuleView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/group_module/group_module.html'

    def __init__(self, **kwargs):
        self.form_groupmodule_submodule = None
        self.form_group_module = None
        self.sub_module_count = None
        self.group_module_all = None
        self.group_module_exist = True
        super().__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.group_module_all = GroupSubModule.current.prefetch_related(
            'group_module')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.form_group_module = GroupModuleForm(auto_id='id_group_module_%s')
        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        total_forms = int(request.POST['groupsubmodule_prefix-TOTAL_FORMS'])
        module = request.POST.get('module')
        self.sub_module_count = SubModule.current.filter(module=module).count()
        initial_list = list()
        for _ in range(total_forms):
            initial_list.append(dict(module=module))
        self.form_group_module = GroupModuleForm(
            request.POST, auto_id='id_group_module_%s')
        self.form_groupmodule_submodule = GroupSubmoduleFormSet(
            request.POST, prefix='groupsubmodule_prefix', initial=initial_list)
        self.group_module_exist = False
        if self.form_group_module.is_valid() and self.form_groupmodule_submodule.is_valid():
            try:
                with transaction.atomic():
                    group_module = self.form_group_module.save(commit=False)
                    self.form_groupmodule_submodule = GroupSubmoduleFormSet(
                        request.POST, instance=group_module,
                        initial=initial_list,
                        prefix='groupsubmodule_prefix')
                    if self.form_groupmodule_submodule.is_valid():
                        group_module.save()
                        self.form_groupmodule_submodule.save()
                        self.form_group_module = GroupModuleForm(
                            auto_id='id_group_module_%s')
                self.group_module_exist = True
                messages.success(request,
                                 core_constants.MESSAGE_TAGS['success'])
            except IntegrityError:
                messages.warning(request,
                                 core_constants.msg_sub_module_duplicate)

        else:
            messages.warning(request, core_constants.MESSAGE_TAGS['warning'])
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_group_module'] = self.form_group_module
        context['list_group_module'] = self.group_module_all
        context['formset_submoduleform'] = self.form_groupmodule_submodule
        context['group_module_exist'] = self.group_module_exist
        context['count_sub_module'] = self.sub_module_count
        return context


class GroupModuleEditView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/group_module/group_module_add.html'

    def __init__(self, **kwargs):
        self.group_module = None
        self.form_group_module = None
        self.form_groupmodule_submodule = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        group_module_pk = request.GET['group_module_pk']
        module = request.GET['module']
        self.group_module = GroupModule.current.get(pk=group_module_pk)
        self.form_group_module = GroupModuleForm(
            auto_id='id_group_module_%s', instance=self.group_module)
        self.sub_module_count = SubModule.current.filter(
            module__text=module).count()
        self.form_groupmodule_submodule = GroupSubmoduleFormSet(
            instance=self.group_module, prefix='groupsubmodule_prefix')

        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        data = loads(request.body.decode('utf-8'))
        data_group_module_pk = data['form_pk']
        data_formset = data['formset']
        module = data['module']
        self.group_module = GroupModule.current.get(pk=data_group_module_pk)
        self.form_group_module = GroupModuleForm(
            auto_id='id_group_module_%s', instance=self.group_module)
        self.sub_module_count = SubModule.current.filter(
            module__text=module).count()
        self.form_groupmodule_submodule = GroupSubmoduleFormSet(
            data_formset, prefix='groupsubmodule_prefix',
            instance=self.group_module)
        if self.form_groupmodule_submodule.is_valid():
            instances = self.form_groupmodule_submodule.save(commit=False)
            for instance in instances:
                instance.save()
            self.form_groupmodule_submodule = GroupSubmoduleFormSet(
                prefix='groupsubmodule_prefix', instance=self.group_module)
            messages.success(request, core_constants.MESSAGE_TAGS['success'])
        else:
            self.form_groupmodule_submodule = GroupSubmoduleFormSet(
                prefix='groupsubmodule_prefix', instance=self.group_module)
            messages.error(request, core_constants.MESSAGE_TAGS['error'])
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_group_module'] = self.form_group_module
        context['formset_submoduleform'] = self.form_groupmodule_submodule
        # context['group_module_exist'] = self.group_module_exist
        context['count_sub_module'] = self.sub_module_count
        context['form_pk'] = self.group_module.id
        context['btn_edit'] = core_constants.BTN_EDIT
        return context


class GroupModuleListView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/group_module/group_module_list.html'

    def get(self, request, *args, **kwargs):
        self.group_module_all = GroupSubModule.current.all().select_related(
            'group_module')
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_group_module'] = self.group_module_all
        return context


class GroupModuleFormsetView(TemplateLoginRequiredMixin):
    template_name = 'administrator/maintenance/group_module/group_submodule_formset.html'

    def __init__(self, **kwargs):
        self.form_groupmodule_submodule = None
        self.group_module_exist = False
        self.group_module_msg = True
        self.sub_module = 0
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        group = request.GET.get('group')
        module = request.GET.get('module')
        group_module = GroupModule.current.filter(module=module,
                                                  group=group).exists()
        if group_module:
            self.group_module_exist = True
            messages.error(request, core_constants.msg_group_module_exist)
        else:
            sub_module = SubModule.current.filter(module=module)
            if sub_module.exists():
                self.sub_module = sub_module.count()
                initial = [dict(module=module)]
                self.form_groupmodule_submodule = GroupSubmoduleFormSet(
                    initial=initial, prefix='groupsubmodule_prefix')
            else:
                self.group_module_exist = True
                messages.warning(request, core_constants.msg_sub_module_exist)

        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_module_exist'] = self.group_module_exist
        context['formset_submoduleform'] = self.form_groupmodule_submodule
        context['count_sub_module'] = self.sub_module
        context['msg_exists'] = self.group_module_msg
        return context
