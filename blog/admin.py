from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'published', 'published_at')
	list_filter = ('published',)
	prepopulated_fields = {'slug': ('title',)}
