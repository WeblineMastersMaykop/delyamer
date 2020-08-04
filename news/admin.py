from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe
from news.models import NewsCategory, News, NewsImage


admin.site.register(NewsCategory)


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 0
    classes = ('grp-collapse grp-closed',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('category', 'image', 'is_active'),
        }),
        ('Текст', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('title', 'body1', 'body2', 'body3'),
        }),
        ('SEO', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('slug', 'seo_title', 'seo_desc', 'seo_kwrds'),
        }),
    )

    list_display = ('image_tag', 'title', 'category', 'is_active', 'created', 'updated')
    list_filter = ('is_active', 'category')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body1', 'body2', 'body3',)
    inlines = (NewsImageInline,)

    class Media:
        js = ('/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              '/static/grappelli/tinymce_setup/tinymce_setup.js')

    def image_tag(self, obj):
        try:
            image_link = obj.image_admin.url
        except:
            image_link = ''
        return mark_safe('<img src="{0}">'.format(image_link))
    image_tag.short_description = 'Предпросмотр'
    image_tag.allow_tags = True
