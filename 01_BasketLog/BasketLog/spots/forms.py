from django import forms
from .models import ArenaFacility, ArenaNearbySpot

class ArenaFacilityForm(forms.ModelForm):
    class Meta:
        model = ArenaFacility
        fields = ['arena_name', 'category', 'review']

class ArenaNearbySpotForm(forms.ModelForm):
    class Meta:
        model = ArenaNearbySpot
        fields = ['arena_name', 'category', 'spot_name', 'review']