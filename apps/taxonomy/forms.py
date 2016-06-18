from django import forms

from .models import Kingdom, Type


class KingdomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = Kingdom
        fields = '__all__'

    def save(self, *args, **kwargs):
        kingdom = super().save(*args, **kwargs)
        return kingdom


class TypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = Type
        fields = '__all__'

    def save(self, *args, **kwargs):
        types = super().save(*args, **kwargs)
        return types

