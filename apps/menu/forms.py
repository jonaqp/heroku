from django import forms
from django.contrib.auth.models import Group

from core.constants import NAME_SELECT_DEFAULT, STATUS_MODEL1, SELECT_DEFAULT
from .models import (
    GroupState, GroupModule, GroupSubModule, SubModule)


class GroupForm(forms.ModelForm):
    current_status = forms.ChoiceField(
        widget=forms.Select(), choices=SELECT_DEFAULT + STATUS_MODEL1,
        required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['current_status'].widget.attrs.update(
            {'class': 'form-control'})
        if self.instance.id:
            group_state = GroupState.current.get(group=self.instance.id)
            self.fields['name'].initial = self.instance.name
            self.fields['current_status'].initial = group_state.current_status

    class Meta:
        model = Group
        fields = ['name']

    def save(self, *arg, **kwargs):
        current_status = self.cleaned_data.get('current_status')
        group = super().save(*arg, **kwargs)
        group_state = GroupState.objects.filter(group=group)
        if group_state.exists():
            group_state = GroupState.objects.get(group=group)
            group_state.current_status = current_status
            group_state.save()
        else:
            GroupState.objects.create(group=group, current_status=current_status)
        group.save()
        return group


class GroupModuleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        self.fields['group'].empty_label = NAME_SELECT_DEFAULT
        self.fields['module'].empty_label = NAME_SELECT_DEFAULT

        if instance:
            self.fields['group'].widget.attrs.update({'disabled': True})
            self.fields['module'].widget.attrs.update({'disabled': True})

    class Meta:
        model = GroupModule
        fields = ['group', 'module']
        widgets = {
            "group": forms.Select(attrs={'class': 'form-control'}),
            "module": forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, *arg, **kwargs):
        group_module = super().save(*arg, **kwargs)
        return group_module


class GroupModuleSubmoduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        initial = kwargs.get('initial')
        if instance:
            module = self.instance.group_module.module
            query = SubModule.current.filter(module=module)
            self.fields['submodule'] = forms.ModelChoiceField(queryset=query)
        if initial:
            module = initial['module']
            query = SubModule.current.filter(module=module)
            self.fields['submodule'] = forms.ModelChoiceField(queryset=query)

        self.fields['submodule'].required = True
        self.fields['submodule'].widget.attrs.update({'class': 'form-control'})
        self.fields['submodule'].empty_label = NAME_SELECT_DEFAULT

    def clean(self):
        cleaned_data = super().clean()
        delete_valid = cleaned_data['DELETE']
        id_submodule = cleaned_data['id']
        if delete_valid:
            GroupSubModule.current.get(pk=id_submodule.id).delete(force=True)
        return cleaned_data

    class Meta:
        model = GroupSubModule
        fields = ['group_module', 'submodule']

    def save(self, *args, **kwargs):
        group_submodule = super().save(*args, **kwargs)
        return group_submodule
