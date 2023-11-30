from django.contrib import admin
from .models import Education, UserProfile, ResearchArea, ResearchProject


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    pass  

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass  

@admin.register(ResearchArea)
class ResearchAreaAdmin(admin.ModelAdmin):
    pass  

@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    pass  
