from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from pages.models import PageDocument, PageImage, PageQuote, PageVideo, Page


class PageDocumentInline(admin.TabularInline):
    model = PageDocument
    extra = 0
    fields = ('title', 'document')
    classes = ('grp-collapse grp-closed',)


class PageImageInline(admin.TabularInline):
    model = PageImage
    extra = 0
    fields = ('image',)
    classes = ('grp-collapse grp-closed',)


#class PageQuoteInline(admin.TabularInline):
#    model = PageQuote
#    extra = 1
#    fields = ('image', 'text', 'author', 'profession')
#    classes = ('grp-collapse grp-closed',)


class PageVideoInline(admin.TabularInline):
    model = PageVideo
    extra = 0
    fields = ('video_link', 'channel_link')
    classes = ('grp-collapse grp-closed',)


@admin.register(Page)
class PageAdmin(DjangoMpttAdmin):
    group_fieldsets = True
    sortable_field_name = 'position'

    fieldsets = (
        (None, {
            'fields': ('parent', 'action', 'is_active'),
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

    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body1', 'body2', 'body3',)

    class Media:
        js = ('/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              '/static/grappelli/tinymce_setup/tinymce_setup.js')

    inlines = (PageDocumentInline, PageVideoInline, PageImageInline)