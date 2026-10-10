from django import forms
from .models import Diary

class DiaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['arena_name'].widget.attrs['class'] = 'diary-select'
        self.fields['home_team_name'].widget.attrs['class'] = 'diary-select'
        self.fields['away_team_name'].widget.attrs['class'] = 'diary-select'

    class Meta:
        model = Diary
        fields = [
            'watch_date', #観戦日
            'arena_name',
            'home_team_name',
            'away_team_name',
            'home_team_score',
            'away_team_score',
            'memory',
            'status',
        ]

        widgets = {
            'watch_date':forms.DateInput(attrs={'type':'date'}),#観戦日をカレンダーから選択する
            'home_team_score':forms.NumberInput(attrs={'min':0}),#０以上の数字を入力
            'away_team_score':forms.NumberInput(attrs={'min':0}),
            'memory':forms.Textarea(attrs={
                'rows':5,
                'placeholder':'感想を入力しましょう'
            }),
            'status':forms.RadioSelect(),
        }

    def clean(self):
        cleaned_data = super().clean()
        home = cleaned_data.get('home_team_name')
        away = cleaned_data.get('away_team_name')

        if home and away and home == away:
            raise forms.ValidationError("ホームチームとアウェイチームは異なるチームを選んでください")
        
        return cleaned_data
   
