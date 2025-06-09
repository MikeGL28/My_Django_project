# basketball/admin.py
from django.contrib import admin
from .models import Player, BasketballGame, PlayerGameStats

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'jersey_number', 'height', 'weight', 'total_points', 'avg_points')
    search_fields = ('full_name', 'position')
    list_filter = ('position',)
    fieldsets = (
        ("Основная информация", {
            'fields': ('full_name', 'position', 'jersey_number', 'photo')
        }),
        ("Статистика", {
            'fields': ('two_pointers', 'three_pointers', 'total_points', 'avg_points')
        }),
        ("Физические данные", {
            'fields': ('height', 'weight'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('total_points', 'avg_points')


@admin.register(BasketballGame)
class BasketballGameAdmin(admin.ModelAdmin):
    list_display = ('date', 'two_pointers', 'three_pointers', 'total_points')
    list_filter = ('date',)
    readonly_fields = ('total_points',)
    search_fields = ('date',)

    def intensity_display(self, obj):
        return obj.get_intensity_display()
    intensity_display.short_description = "Интенсивность"

    def description_short(self, obj):
        return obj.description[:50] + "..." if obj.description and len(obj.description) > 50 else obj.description
    description_short.short_description = "Описание"

admin.site.register(PlayerGameStats)