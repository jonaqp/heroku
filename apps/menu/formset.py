from __future__ import unicode_literals

from django.forms import inlineformset_factory

from .forms import GroupModuleSubmoduleForm
from .models import (
    GroupModule, GroupSubModule)

GroupSubmoduleFormSet = inlineformset_factory(
    GroupModule, GroupSubModule, form=GroupModuleSubmoduleForm,
    min_num=1, extra=0,  can_delete=True, can_order=True)
