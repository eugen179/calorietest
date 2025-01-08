from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Food(models.Model):
    name = models.CharField(max_length=100)
    calorie_count = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class DailyCalorieRecord(models.Model):
    date = models.DateField(auto_now_add=True)
    food_items = models.ManyToManyField(Food)
    total_calories = models.PositiveIntegerField(default=0)

    def update_total_calories(self):
        self.total_calories = sum(food.calorie_count for food in self.food_items.all())
        self.save()

    def __str__(self):
        return f"Record for {self.date}"

@receiver(post_save, sender=Food)
def update_daily_record(sender, instance, created, **kwargs):
    if created:
        
        record, _ = DailyCalorieRecord.objects.get_or_create(date=timezone.now().date())
        record.food_items.add(instance)
        record.update_total_calories()  
