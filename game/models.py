from django.db import models

# Create your models here.

class Rule(models.Model):
    title = models.CharField(max_length=200, default="Game Rule")
    description = models.TextField(default="Rule description")

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Team(models.Model):
    name = models.CharField(max_length=100)
    round1_score = models.IntegerField(default=0)
    round2_score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    normalized_score = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def calculate_total(self):
        self.total_score = self.round1_score + self.round2_score
        self.save()

class Card(models.Model):
    number = models.IntegerField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_revealed = models.BooleanField(default=False)

    def __str__(self):
        return f"Card {self.number} - {self.category.name}"

    class Meta:
        ordering = ['number']
