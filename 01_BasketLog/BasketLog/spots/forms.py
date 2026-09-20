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
            "kids_space": forms.RadioSelect(),
            "diaper_table": forms.RadioSelect(),
            "nursing_room": forms.RadioSelect(),
            "category":forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['kids_space', 'diaper_table', 'nursing_room']:
            self.fields[field_name].choices = [
                ('', '入力しない'),
                (1, '有'),
                (2, '無'),
            ]

#class ArenaFacilityImageForm(forms.ModelForm):
    #class Meta:
        #model = ArenaFacilityImage
        #fields = [ "image"]


class ArenaNearbySpotForm(forms.ModelForm):
    class Meta:
        model = ArenaNearbySpot
        fields = [
            'category',
            'spot_name',
            'review',
        ]

        widgets = {
            "spot_name":forms.TextInput(attrs={
                "class": "form-control"
            }),
            "category":forms.RadioSelect(),
            "review":forms.Textarea(attrs={
                "class":"form-control",
                "rows":6,
            }),
        }


#class ArenaNearbyImageForm(forms.ModelForm):
    #class Meta:
        #model = ArenaNearbyImage
        #fields = ["image"]