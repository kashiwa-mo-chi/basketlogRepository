from django.contrib import admin
from .models import Arena_Category, ArenaFacility, Spot_Category, ArenaNearbySpot

@admin.register(Arena_Category)
class Arena_Categoryadmin(admin.ModelAdmin):
    list_display = (
        'id',
        'arena_category',
        'created_at',
        'updated_at'
    )

@admin.register(ArenaFacility)
class ArenaFacilityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'arena_name',
        'category',
        'user',
        'get_kids_space_display',
        'get_diaper_table_display',
        'get_nursing_room_display',
        'created_at',
        'updated_at'
        )

@admin.register(Spot_Category)
class Spot_CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'spot_category',
        'created_at',
        'updated_at'
    )

@admin.register(ArenaNearbySpot)
class ArenaNearbySpotAdmin(admin.ModelAdmin):
    list_display = (
    'id',
    'arena_name',
    'category',
    'user',
    'spot_name',
    'created_at',
    'updated_at')