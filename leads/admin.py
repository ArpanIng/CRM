from django.contrib import admin

from .models import User, UserProfile, Agent, Category, Lead

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(Category)
admin.site.register(Lead)
