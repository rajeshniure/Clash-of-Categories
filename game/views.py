from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Rule, Category, Team, Card
from django.views.decorators.csrf import csrf_exempt
import json

def landing_page(request):
    rules = Rule.objects.all()
    return render(request, 'game/landing.html', {'rules': rules})

def game_board(request):
    cards = Card.objects.all().select_related('category')
    return render(request, 'game/game_board.html', {'cards': cards})

@csrf_exempt
def reveal_card(request, card_id):
    if request.method == 'POST':
        try:
            card = Card.objects.get(id=card_id)
            card.is_revealed = True
            card.save()
            return JsonResponse({
                'success': True,
                'category': card.category.name
            })
        except Card.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Card not found'}, status=404)

@csrf_exempt
def reset_card(request, card_id):
    if request.method == 'POST':
        try:
            card = Card.objects.get(id=card_id)
            card.is_revealed = False
            card.save()
            return JsonResponse({
                'success': True,
                'card_number': card.number
            })
        except Card.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Card not found'}, status=404)

def timer_page(request):
    return render(request, 'game/timer.html')

def scoring_page(request):
    teams = Team.objects.all()
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            team_id = data.get('team_id')
            round1_score = data.get('round1_score')
            round2_score = data.get('round2_score')
            
            if not team_id:
                return JsonResponse({'success': False, 'error': 'Team ID is required'})
            
            try:
                team = Team.objects.get(id=team_id)
            except Team.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Team not found'}, status=404)
            
            if round1_score is not None:
                team.round1_score = round1_score
            if round2_score is not None:
                team.round2_score = round2_score
            team.calculate_total()
            
            # Normalize scores
            max_score = Team.objects.all().order_by('-total_score').first().total_score
            if max_score > 0:
                for t in Team.objects.all():
                    t.normalized_score = (t.total_score / max_score) * 24
                    t.save()
            
            return JsonResponse({'success': True})
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return render(request, 'game/scoring.html', {'teams': teams})

@csrf_exempt
def add_team(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        team_name = data.get('name')
        
        if team_name:
            team = Team.objects.create(name=team_name)
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@csrf_exempt
def delete_team(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        team_id = data.get('team_id')
        
        try:
            team = Team.objects.get(id=team_id)
            team.delete()
            return JsonResponse({'success': True})
        except Team.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})

def reset_points(request):
    if request.method == 'POST':
        try:
            # Reset all teams' scores to zero
            Team.objects.all().update(
                round1_score=0,
                round2_score=0,
                total_score=0,
                normalized_score=0
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
