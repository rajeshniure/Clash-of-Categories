from django.contrib import admin
from .models import Rule, Category, Team, Card

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ['title']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ['name']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'round1_score', 'round2_score', 'total_score', 'normalized_score')
    readonly_fields = ('total_score', 'normalized_score')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('number', 'category', 'is_revealed')
    list_filter = ('is_revealed',)
    search_fields = ['category__name']
