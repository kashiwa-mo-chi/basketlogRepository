from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ArenaFacility, ArenaNearbySpot, ArenaFacilityImage
from .forms import ArenaFacilityForm, ArenaNearbySpotForm
from games.models import Diary

def arena_list(request):
    arenas = Diary.ARENA_CHOICES

    query = request.GET.get('q', '')

    if query:
        arenas = [
            (arena_id, arena_name)
            for arena_id, arena_name in arenas
            if query in arena_name
        ]

    return render(request, 'spots/arena_list.html', {
        'arenas': arenas,
        'query': query,
    })


def arena_top(request, arena_id):
    """アリーナ詳細ページ"""

    # アリーナ内情報
    facilities = ArenaFacility.objects.filter(
        arena_name=arena_id
    ).order_by("-created_at")

    # 周辺情報
    nearby_spots = ArenaNearbySpot.objects.filter(
        arena_name=arena_id
    ).order_by("-created_at")

    # 設備アンケート集計
    total = facilities.count()

    kids_yes = facilities.filter(kids_space=1).count()
    diaper_yes = facilities.filter(diaper_table=1).count()
    nursing_yes = facilities.filter(nursing_room=1).count()

    kids_rate = int(kids_yes / total * 100) if total else 0
    diaper_rate = int(diaper_yes / total * 100) if total else 0
    nursing_rate = int(nursing_yes / total * 100) if total else 0

    # 最新口コミ5件
    recent_posts = facilities[:5]

    # アリーナ名
    arena_name = dict(Diary.ARENA_CHOICES).get(arena_id, "")

    context = {
        "arena_id": arena_id,
        "arena_name": arena_name,

        # 投稿
        "facilities": facilities,
        "nearby_spots": nearby_spots,

        # 集計
        "total": total,
        "kids_yes": kids_yes,
        "diaper_yes": diaper_yes,
        "nursing_yes": nursing_yes,
        "kids_rate": kids_rate,
        "diaper_rate": diaper_rate,
        "nursing_rate": nursing_rate,

        # 最新口コミ
        "recent_posts": recent_posts,
    }

    return render(request, "spots/arena_top.html", context)

@login_required
def facility_post_create(request, arena_id):
    arena_name = dict(Diary.ARENA_CHOICES).get(arena_id)
    """アリーナ内情報の新規投稿"""
    if request.method == 'POST':
        form = ArenaFacilityForm(request.POST, request.FILES)

        images = request.FILES.getlist("images")

        if len(images) > 5:
            form.add_error(None, "画像は５枚まで投稿できます")

        elif form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.arena_name = arena_id 
            post.save()

            for image in images:
                ArenaFacilityImage.objects.create(
                    arena_facility=post,
                    image=image
                )

            return redirect('spots:arena_top', arena_id=arena_id)
    else:
        form = ArenaFacilityForm()

        
    return render(request, 'spots/arena_form.html', {
        'form': form, 
        'title': 'アリーナ内情報の投稿',
        'arena_id': arena_id,
        'arena_name': arena_name,
    })

@login_required
def nearby_post_create(request, arena_id):
    """アリーナ周辺情報の新規投稿"""
    arena_name = dict(Diary.ARENA_CHOICES).get(arena_id)
    
    if request.method == 'POST':
        form = ArenaNearbySpotForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.arena_name = arena_id # URLから届いたアリーナIDを自動固定
            post.save()
            return redirect('spots:arena_top', arena_id=arena_id)
    else:
        form = ArenaNearbySpotForm()
        
    return render(request, 'spots/post_form.html', {
        'form': form,
        'title': 'アリーナ周辺情報の投稿',
        'arena_id': arena_id,
        'arena_name': arena_name,
    })
