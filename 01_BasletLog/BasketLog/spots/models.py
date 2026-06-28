from django.db import models
from django.contrib.auth import get_user_model
from games.models import Diary
ARENA_CHOICES = Diary.ARENA_CHOICES

User = get_user_model()

class Arena_Category(models.Model):
    arena_category = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='カテゴリ名'
    )
    created_at=models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at=models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        db_table = 'arena_category'
        verbose_name = 'アリーナカテゴリ'
        verbose_name_plural = 'アリーナカテゴリ'

    def __str__(self):
        return self.arena_category

class Arena_Facility(models.Model):

    FACILITY_CHOICES = [
        (1, '有'),
        (2, '無'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        verbose_name="投稿者",
    )

    category = models.ForeignKey(
        Arena_Category,
        on_delete=models.PROTECT,
        verbose_name="アリーナカテゴリ"
    )

    arena_name = models.IntegerField(
        choices=ARENA_CHOICES,
        default=1,
        verbose_name="アリーナ名",
    )

    kids_space = models.ImageField(
        choices=FACILITY_CHOICES,
        default=2,
        verbose_name="キッズスペース"
    )

    diaper_table = models.IntegerField(
        choices=FACILITY_CHOICES,
        default=2,
        verbose_name="おむつ交換台"
    )

    nursing_room = models.IntegerField(
        choices=FACILITY_CHOICES,
        default=2,
        verbose_name="授乳室"
    )

    review=models.CharField(
        max_length=1000,
        verbose_name="コメント"
    )

    created_at=models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at=models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        db_table = 'arena_facilities'
        verbose_name = 'アリーナ情報'
        verbose_name_plural = 'アリーナ情報'

    def __str__(self):
        return f"{self.get_arena_name_display()} [{self.category.arena_category}] ({self.user.username})"
    
class Spot_Category(models.Model):
    spot_category = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='カテゴリ名'
    )
    created_at=models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at=models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        db_table = 'spot_category'
        verbose_name = '周辺施設カテゴリ'
        verbose_name_plural = '周辺施設カテゴリ'

    def __str__(self):
        return self.spot_category
    

class Arena_Nearby_Spot(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        verbose_name="投稿者",
    )

    arena_name = models.IntegerField(
        choices=ARENA_CHOICES,
        default=1,
        verbose_name="アリーナ名",
    )

    category = models.ForeignKey(
        Spot_Category, 
        on_delete=models.PROTECT, 
        verbose_name="周辺カテゴリ"
    )

    spot_name = models.CharField(
        max_length=30,
        verbose_name="スポット名",
    )

    review = models.CharField(
        max_length=1000,
        verbose_name="見どころ"
    )

    created_at=models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at=models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        db_table = 'arena_nearby_spots'
        verbose_name = 'アリーナ周辺施設情報'
        verbose_name_plural = 'アリーナ周辺施設情報'

    def __str__(self):
        return f"{self.get_arena_name_display()} [{self.category.spot_category}] {self.spot_name} ({self.user.username})"