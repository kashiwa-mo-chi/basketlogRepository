from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DiaryForm, DiaryPictureFormSet
from django.contrib.auth import get_user_model
from .models import Diary

@login_required
def diary_create(request):
    if request.method == 'POST':
        diary_form = DiaryForm(request.POST) #保存ボタンPOSTが押された時の処理
        picture_formset = DiaryPictureFormSet(request.POST, request.FILES)

        if diary_form.is_valid() and picture_formset.is_valid():
            diary = diary_form.save(commit=False)
            diary.user = request.user
            diary.save()

            picture_formset.instance = diary
            picture_formset.save()

            return redirect('games:diary_detail', diary_id=diary.id) #投稿が完了したら飛ぶベージ、観戦記録詳細画面へ遷移
               
    else:
        diary_form = DiaryForm()
        picture_formset = DiaryPictureFormSet()

    context = {
        'diary_form': diary_form,
        'picture_formset': picture_formset,
    }
    return render(request, 'games/diary_form.html', context)

def diary_detail(request, diary_id):
    diary = get_object_or_404(Diary, id=diary_id)

    context = {
        'diary':diary,        
    }
    return render(request, 'games/diary_detail.html', context)
