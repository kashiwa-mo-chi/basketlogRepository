from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django .core.paginator import Paginator
from django.db.models import Q
from .forms import DiaryForm
from django.contrib.auth import get_user_model
from .models import Diary, DiaryPicture

#MY観戦記録一覧画面
@login_required
def diary_list(request):
    diaries = Diary.objects.filter(user=request.user).order_by('-watch_date')

    # 検索機能
    query = request.GET.get('q')
    date_query = request.GET.get('date')

    if query:
        condition = Q(memory__icontains=query)

        team_choices = Diary._meta.get_field('home_team_name').choices
        for num, name in team_choices:
            if query in name:
                condition |= Q(home_team_name=num) | Q(away_team_name=num)

    # 会場名（ARENA_CHOICES）から文字が一致する「数字」を探す
        arena_choices = Diary._meta.get_field('arena_name').choices
        for num, name in arena_choices:
            if query in name:
                condition |= Q(arena_name=num)

        diaries = diaries.filter(condition)

    if date_query:
        diaries = diaries.filter(watch_date=date_query)

    paginator = Paginator(diaries, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'games/diary_list.html', {'page_obj': page_obj})

@login_required
def diary_create(request):
    if request.method == 'POST':
        diary_form = DiaryForm(request.POST) 
        images = request.FILES.getlist("images")

        if diary_form.is_valid():
            diary = diary_form.save(commit=False)
            diary.user = request.user
            diary.save()

            for image in images:
                DiaryPicture.objects.create(
                    diary=diary,
                    picture_url=image
                )

            return redirect('games:diary_detail', diary_id=diary.id)
               
    else:
        diary_form = DiaryForm()

    context = {
        'diary_form': diary_form,
    }
    return render(request, 'games/diary_form.html', context)

#詳細画面
def diary_detail(request, diary_id):
    diary = get_object_or_404(Diary, id=diary_id)
    return render(request, 'games/diary_detail.html', {'diary':diary})

#みんなの観戦記録一覧
def public_diary_list(request):
    diaries = Diary.objects.filter(status=1).order_by('-watch_date')

    # 検索機能
    query = request.GET.get('q')
    date_query = request.GET.get('date')

    if query:
        condition = Q(memory__icontains=query)

        team_choices = Diary._meta.get_field('home_team_name').choices
        for num, name in team_choices:
            if query in name:
                condition |= Q(home_team_name=num) | Q(away_team_name=num)

        arena_choices = Diary._meta.get_field('arena_name').choices
        for num, name in arena_choices:
            if query in name:
                condition |= Q(arena_name=num)

        diaries = diaries.filter(condition)

    if date_query:
        diaries = diaries.filter(watch_date=date_query)
    
    paginator = Paginator(diaries, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'games/public_diary_list.html', {'page_obj': page_obj})

@login_required
def diary_update(request, diary_id):
    """観戦記録編集"""

    diary = get_object_or_404(Diary, id=diary_id)

    if diary.user != request.user:
        return redirect("games:diary_detail", diary_id=diary.id)

    if request.method == "POST":
        diary_form = DiaryForm(request.POST, instance=diary)
        
        if diary_form.is_valid():
            diary_form.save()

            delete_ids = request.POST.getlist("delete_images")
            print("削除する画像ID:", delete_ids)

            DiaryPicture.objects.filter(
                id__in=delete_ids,
                diary=diary
            ).delete()

            images = request.FILES.getlist("images")

            for image in images:
                DiaryPicture.objects.create(
                    diary=diary,
                    picture_url=image
        )

            return redirect("games:diary_detail", diary_id=diary.id)

    else:
        diary_form = DiaryForm(instance=diary)
        pictures = diary.pictures.all()

    context = {
        "diary_form": diary_form,
        "pictures": pictures,
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