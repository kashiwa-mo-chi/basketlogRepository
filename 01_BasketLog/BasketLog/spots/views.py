from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ArenaFacility, ArenaNearbySpot
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


def spot_top(request, arena_id):
    """特定のアリーナの口コミ詳細画面"""
    # データを取得（新着順）
    facilities = ArenaFacility.objects.filter(arena_name=arena_id).order_by('-created_at')
    nearby_spots = ArenaNearbySpot.objects.filter(arena_name=arena_id).order_by('-created_at')
    
    # 選択されたアリーナの名前を表示用に探す
    arena_dict = dict(Diary.ARENA_CHOICES)
    arena_name = arena_dict.get(arena_id, "")
            
    return render(request, 'spots/spot_top.html', {
        'facilities': facilities,
        'nearby_spots': nearby_spots,
        'arena_id': arena_id,
        'arena_name': arena_name,
    })

@login_required
def facility_post_create(request, arena_id):
    """アリーナ内情報の新規投稿"""
    if request.method == 'POST':
        form = ArenaFacilityForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.arena_name = arena_id # URLから届いたアリーナIDを自動固定
            post.save()
            return redirect('spots:spot_top', arena_id=arena_id)
    else:
        form = ArenaFacilityForm(initial={'arena_name': arena_id})
        
    return render(request, 'spots/post_form.html', {'form': form, 'title': 'アリーナ内情報の投稿', 'arena_id': arena_id})

@login_required
def nearby_post_create(request, arena_id):
    """アリーナ周辺情報の新規投稿"""
    
    if request.method == 'POST':
        form = ArenaNearbySpotForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.arena_name = arena_id # URLから届いたアリーナIDを自動固定
            post.save()
            return redirect('spots:spot_top', arena_id=arena_id)
    else:
        form = ArenaNearbySpotForm(initial={'arena_name': arena_id})
        
    return render(request, 'spots/post_form.html', {'form': form, 'title': 'アリーナ周辺情報の投稿', 'arena_id': arena_id})
