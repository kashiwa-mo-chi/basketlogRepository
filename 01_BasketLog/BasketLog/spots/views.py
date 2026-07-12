from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ArenaFacility, ArenaNearbySpot, ArenaFacilityImage, ArenaNearbyImage
from .forms import ArenaFacilityForm, ArenaNearbySpotForm
from games.models import Diary
from django.contrib import messages

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

def facility_detail(request, pk):
    post = get_object_or_404(
        ArenaFacility,
        pk=pk
    )

    context = {
        "post":post,        
    }

    return render(
        request,
        "spots/facility_detail.html",
        context
    )

@login_required
def facility_post_update(request, pk):
    """アリーナ内情報の編集"""

    post = get_object_or_404(ArenaFacility, pk=pk)

    # 投稿者以外は編集できない
    if post.user != request.user:
        return redirect("spots:facility_detail", pk=pk)

    if request.method == "POST":
        form = ArenaFacilityForm(request.POST, instance=post)
                 
        files = request.FILES.getlist("images")

        current_count = post.images.count()

        if current_count + len(files) > 5:
            form.add_error(None, "画像は５枚まで投稿できます")
        
        elif form.is_valid():
            post = form.save()

            for file in files:
                ArenaFacilityImage.objects.create(
                    arena_facility=post,
                    image=file
                )
            return redirect("spots:facility_detail", pk=post.pk)
            
    else:
        form = ArenaFacilityForm(instance=post)

    arena_name = dict(Diary.ARENA_CHOICES).get(post.arena_name)

    images = post.images.all()

    return render(request, "spots/arena_form.html", {
        "form": form,
        "title": "アリーナ内情報の編集",
        "arena_id": post.arena_name,
        "arena_name": arena_name,
        "images": images,
    })



@login_required
def facility_post_delete(request, pk):
    """アリーナ情報投稿の削除"""

    post = get_object_or_404(ArenaFacility, pk=pk)

    # 投稿者のみ削除可能
    if post.user != request.user:
        return redirect("spots:facility_detail", pk=pk)

    if request.method == "POST":
        arena_id = post.arena_name
        post.delete()
        return redirect("spots:arena_top", arena_id=arena_id)

    return redirect("spots:facility_detail", pk=pk)

@login_required
def facility_image_delete(request, image_pk):
    """アリーナ内情報の写真削除"""

    image = get_object_or_404(ArenaFacilityImage, pk=image_pk)

    # 投稿者本人以外は削除不可
    if image.arena_facility.user != request.user:
        return redirect(
            "spots:facility_detail",
            pk=image.arena_facility.pk
        )

    facility_pk = image.arena_facility.pk

    if request.method == "POST":
        image.delete()

    return redirect("spots:facility_post_update", pk=facility_pk)

def nearby_list(request, arena_id):
    nearby_spots = ArenaNearbySpot.objects.filter(
        arena_name=arena_id
    ).select_related(
        "category",
        "user"
    ).order_by("-created_at")

    arena_name =dict(Diary.ARENA_CHOICES).get(arena_id)

    return render(
        request,
        "spots/nearby_list.html",
        {
            "arena_id":arena_id,
            "arena_name":arena_name,
            "nearby_spots":nearby_spots,
        },
    )

@login_required
def nearby_create(request, arena_id):
    """アリーナ周辺情報の新規投稿"""
    arena_name = dict(Diary.ARENA_CHOICES).get(arena_id)
    
    if request.method == 'POST':
        form = ArenaNearbySpotForm(request.POST, request.FILES)

        images =  request.FILES.getlist("images")

        if len(images) > 5:
            form.add_error(None, "画像は５枚まで投稿できます")
        
        elif form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.arena_name = arena_id # URLから届いたアリーナIDを自動固定
            post.save()

            for image in images:
                ArenaNearbyImage.objects.create(
                    arena_nearby=post,
                    image=image
                )

            return redirect('spots:nearby_detail', post.pk)
    else:
        form = ArenaNearbySpotForm()
        
    return render(request, 'spots/nearby_form.html', {
        'form': form,
        'title': 'アリーナ周辺情報の投稿',
        'arena_id': arena_id,
        'arena_name': arena_name,
    })

@login_required
def nearby_detail(request, pk):
    nearby = get_object_or_404(
        ArenaNearbySpot,
        pk=pk
    )

    return render(
        request,
        "spots/nearby_detail.html",
        {
            "nearby": nearby,
        },
    )

@login_required
def nearby_update(request, pk):
    """アリーナ周辺情報の編集"""

    post = get_object_or_404(ArenaNearbySpot, pk=pk)

    # 投稿者以外は編集できない
    if post.user != request.user:
        return redirect("spots:nearby_detail", pk=pk)

    if request.method == "POST":
        form = ArenaNearbySpotForm(
            request.POST, 
            request.FILES,
            instance=post
        )

        images = request.FILES.getlist("images")

        existing_count = post.images.count()

        if existing_count + len(images) >5:
            form.add_error(None, "画像は５枚まで投稿できます")

        elif form.is_valid():
            form.save()

            for image in images:
                ArenaNearbyImage.objects.create(
                    arena_nearby=post,
                    image=image,
                )

            return redirect("spots:nearby_detail", pk=post.pk)

    else:
        form = ArenaNearbySpotForm(instance=post)

    images = post.images.all()

    arena_name = dict(Diary.ARENA_CHOICES).get(post.arena_name)

    return render(request, "spots/nearby_form.html", {
        "form": form,
        "images":images,
        "title": "アリーナ周辺情報の編集",
        "arena_id": post.arena_name,
        "arena_name": arena_name,
    })

@login_required
def nearby_delete(request, pk):
    post = get_object_or_404(ArenaNearbySpot, pk=pk)

    if post.user != request.user:
        return redirect("spots:nearby_detail", pk=pk)
    
    if request.method == "POST":
        arena_id = post.arena_name
        post.delete()
        return redirect("spots:nearby_list", arena_id=arena_id)
    
    return redirect("spots:nearby_detail", pk=pk)

@login_required
def nearby_image_delete(request, image_pk):
    image = get_object_or_404(ArenaNearbyImage, pk=image_pk)

    if image.arena_nearby.user != request.user:
        return redirect(
            "spots:nearby_detail",
            pk=image.arena_nearby.pk
        )
    
    nearby_pk = image.arena_nearby.pk

    if request.method == "POST":
        image.delete()

    return redirect("spots:nearby_update", pk=nearby_pk)
    