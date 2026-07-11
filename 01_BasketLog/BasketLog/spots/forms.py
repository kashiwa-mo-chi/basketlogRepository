from django import forms
from .models import ArenaFacility, ArenaNearbySpot
from .models import ArenaFacilityImage

class ArenaFacilityForm(forms.ModelForm):
    class Meta:
        model = ArenaFacility
        fields = [
            'category',
            'kids_space',
            'diaper_table',
            'nursing_room',
            'review'
        ]
            
        widgets = {
            "kids_space": forms.RadioSelect,
            "diaper_table": forms.RadioSelect,
            "nursing_room": forms.RadioSelect,
        }

#class ArenaFacilityImageForm(forms.ModelForm):
    #class Meta:
        #model = ArenaFacilityImage
        #fields = [ "image"]


class ArenaNearbySpotForm(forms.ModelForm):
    class Meta:
        model = ArenaNearbySpot
        fields = ['category', 'spot_name', 'review']

#class ArenaNearbyImageForm(forms.ModelForm):
    #class Meta:
        #model = ArenaNearbyImage
        #fields = ["image"]