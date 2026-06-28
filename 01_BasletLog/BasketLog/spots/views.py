from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ArenaFacility, ArenaNearbySpot
from .forms import ArenaFacilityForm, ArenaNearbySpotForm

def spot_top(request):
    selected_arena = request.GET.get('arena_name')
    
    # データを取得（新着順）
    facilities = ArenaFacility.objects.all().order_by('-created_at')
    nearby_spots = ArenaNearbySpot.objects.all().order_by('-created_at')
    
    # もしアリーナが選ばれていたら、そのアリーナの口コミだけに絞り込む
    if selected_arena:
        # choicesの保存値（1, 2, 3...など）が文字列として届くため、intに変換して比較
        facilities = facilities.filter(arena_name=selected_arena)
        nearby_spots = nearby_spots.filter(arena_name=selected_arena)
        
    return render(request, 'spots/spot_top.html', {
        'facilities': facilities,
        'nearby_spots': nearby_spots,
        'selected_arena': selected_arena,
    })

@login_required
def facility_post_create(request):
    """アリーナ内情報の新規投稿"""
    if request.method == 'POST':
        form = ArenaFacilityForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user # ログイン中のユーザーを自動セット
            post.save()
            return redirect('spots:spot_top')
    else:
        # もしアリーナが選択された状態で投稿ボタンが押されていたら、初期値としてセット
        initial_arena = request.GET.get('arena_name')
        form = ArenaFacilityForm(initial=({'arena_name': initial_arena} if initial_arena else None))
        
    return render(request, 'spots/post_form.html', {'form': form, 'title': 'アリーナ内情報の投稿'})

@login_required
def nearby_post_create(request):
    """アリーナ周辺情報の新規投稿"""
    if request.method == 'POST':
        form = ArenaNearbySpotForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('spots:spot_top')
    else:
        initial_arena = request.GET.get('arena_name')
        form = ArenaNearbySpotForm(initial=({'arena_name': initial_arena} if initial_arena else None))
        
    return render(request, 'spots/post_form.html', {'form': form, 'title': 'アリーナ周辺情報の投稿'})