from django.shortcuts import render, redirect
#from django.contrib.auth.decorators import login_required
from .forms import DiaryForm, DiaryPictureFormSet
from django.contrib.auth import get_user_model


#@login_required
def diary_create(request):
    if request.method == 'POST':
        diary_form = DiaryForm(request.POST) #保存ボタンPOSTが押された時の処理
        picture_formset = DiaryPictureFormSet(request.POST, request.FILES)

        #if diary_form.is_valid() and picture_formset.is_valid():
            #diary = diary_form.save(commit=False)
            #diary.user = request.user
            #diary.save()

            #picture_formset.instance = diary
            #picture_formset.save()

            #return redirect('games:diary_list') #投稿が完了したら飛ぶベージ

        if diary_form.is_valid() and picture_formset.is_valid():
            diary = diary_form.save(commit=False)
            
            # --- 【一時的な修正】ログイン機能がない間のための処理 ---
            User = get_user_model()
            # データベースに登録されている最初のユーザー（管理者など）を自動でセットします
            # もし一人もユーザーがいない場合はエラーになるため、管理画面などで一人作成しておく必要があります
            diary.user = User.objects.first() 
            # ----------------------------------------------------
            
            diary.save()
            picture_formset.instance = diary
            picture_formset.save()

            return redirect('games:diary_create')  # 一覧がないので、一旦投稿画面自身にリダイレクトさせます
        
    else:
        diary_form = DiaryForm()
        picture_formset = DiaryPictureFormSet()

    context = {
        'diary_form': diary_form,
        'picture_formset': picture_formset,
    }
    return render(request, 'games/diary_form.html', context)
