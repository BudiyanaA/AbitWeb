from django.contrib import admin
from .models import Post, Comment, Image

### admin detail
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','category','created_at','author')
    list_filter = ("category","author",)
    search_fields = ['title', 'content']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Image)
