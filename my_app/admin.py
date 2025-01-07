from django.contrib import admin
from .models import Food, DailyCalorieRecord

class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'calorie_count')  
    search_fields = ('name',)  

class DailyCalorieRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_calories')  
    list_filter = ('date',)  
    filter_horizontal = ('food_items',)  


admin.site.register(Food, FoodAdmin)
admin.site.register(DailyCalorieRecord, DailyCalorieRecordAdmin)
 