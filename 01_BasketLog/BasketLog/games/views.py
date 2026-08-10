from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django .core.paginator import Paginator
from django.db.models import Q
from .forms import DiaryForm, DiaryPictureFormSet
from django.contrib.auth import get_user_model
from .models import Diary

#MY観戦記録一覧画面
@login_required
def diary_list(request):
    diaries = Diary.objects.filter(user=request.user).order_by('-watch_date')

    #検索機能
    query = request.GET.get('q')
    if query:
        condition = Q(memory__icontains=query)

        condition |= Q(watch_date__contains=query)

        team_choices = Diary._meta.get_field('home_team_name').choices
        for num, name in team_choices:
            if query in name:  
                condition |= Q(home_team_name=num) | Q(away_team_name=num)

        # 3. 会場名（ARENA_CHOICES）から文字が一致する「数字」を探す
        arena_choices = Diary._meta.get_field('arena_name').choices
        for num, name in arena_choices:
            if query in name:  
                condition |= Q(arena_name=num)

        # 最後に、まとめた条件でデータを一気に絞り込む
        diaries = diaries.filter(condition)
    
    paginator = Paginator(diaries, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'games/diary_list.html', {'page_obj': page_obj})

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

#詳細画面
def diary_detail(request, diary_id):
    diary = get_object_or_404(Diary, id=diary_id)
    return render(request, 'games/diary_detail.html', {'diary':diary})

#みんなの観戦記録一覧
def public_diary_list(request):
    diaries = Diary.objects.filter(status=1).order_by('-watch_date')

    #検索機能
    query = request.GET.get('q')
    if query:
        condition = Q(memory__icontains=query)

        condition |= Q(watch_date__contains=query)

        team_choices = Diary._meta.get_field('home_team_name').choices
        for num, name in team_choices:
            if query in name:  
                condition |= Q(home_team_name=num) | Q(away_team_name=num)

       
        arena_choices = Diary._meta.get_field('arena_name').choices
        for num, name in arena_choices:
            if query in name: 
                condition |= Q(arena_name=num)

        
        diaries = diaries.filter(condition)
    
    paginator = Paginator(diaries, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'games/public_diary_list.html', {'page_obj': page_obj})
@login_required
def diary_update(request, diary_id):
    """観戦記録編集"""

    diary = get_object_or_404(Diary, id=diary_id)

    # 投稿者以外は編集できない
    if diary.user != request.user:
        return redirect("games:diary_detail", diary_id=diary.id)

    if request.method == "POST":
        diary_form = DiaryForm(request.POST, instance=diary)
        picture_formset = DiaryPictureFormSet(
            request.POST,
            request.FILES,
            instance=diary
        )

        if diary_form.is_valid() and picture_formset.is_valid():
            diary_form.save()
            picture_formset.save()

            return redirect("games:diary_detail", diary_id=diary.id)

    else:
        diary_form = DiaryForm(instance=diary)
        picture_formset = DiaryPictureFormSet(instance=diary)

    context = {
        "diary_form": diary_form,
        "picture_formset": picture_formset,
        "is_edit": True,
    }

    return render(request, "games/diary_form.html", context)

@login_required
def diary_delete(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)

    # 投稿者以外は削除できない
    if diary.user != request.user:
        return redirect("games:diary_detail", diary_id=diary_id)

    if request.method == "POST":
        diary.delete()

    return redirect("games:diary_list")