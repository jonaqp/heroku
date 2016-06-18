from django import forms

from .models import Container, Trip


class ContainerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContainerForm, self).__init__(*args, **kwargs)
        self.fields['identifier_mac'].widget.attrs.update(
            {'placeholder': 'Identifier mac', 'required': True,
             'class': 'form-control'})
        self.fields['name_mac'].widget.attrs.update(
            {'placeholder': 'Identifier mac', 'class': 'form-control'})
        self.fields['number_mac'].widget.attrs.update(
            {'placeholder': 'Number mac', 'class': 'form-control'})
        self.fields['port'].widget.attrs.update(
            {'placeholder': 'Port', 'class': 'form-control'})
        self.fields['zone'].widget.attrs.update(
            {'placeholder': 'Zone', 'class': 'form-control'})
        self.fields['country'].widget.attrs.update(
            {'placeholder': 'Country', 'class': 'form-control'})
        self.fields['fisher'].widget.attrs.update(
            {'placeholder': 'Fisher', 'class': 'form-control'})

    class Meta:
        model = Container
        fields = ['identifier_mac', 'name_mac', 'number_mac',
                  'port', 'zone', 'country', 'fisher']

    def save(self, commit=True):
        container = super(ContainerForm, self).save(commit=False)
        if commit:
            container.save()
        return container


class TripForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['container'].widget.attrs.update(
            {'placeholder': 'container', 'class': 'form-control'})
        self.fields['datetime_image'].widget.attrs.update(
            {'placeholder': 'Datetime Image', 'class': 'form-control'})
        self.fields['picture'].widget.attrs.update(
            {'placeholder': 'Picture', 'class': 'form-control'})
        self.fields['latitude'].widget.attrs.update(
            {'placeholder': 'Latitude', 'class': 'form-control'})
        self.fields['longitude'].widget.attrs.update(
            {'placeholder': 'Longitude', 'class': 'form-control'})

    class Meta:
        model = Trip
        fields = ['container',
                  'datetime_image',
                  'picture', 'latitude', 'longitude']

    def save(self, commit=True):
        trip = super(TripForm, self).save(commit=False)
        if commit:
            trip.save()
        return trip
