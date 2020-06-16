from django.contrib import admin
from core.models import MailFromString, MailToString, TitleTag, Index


admin.site.register(MailFromString)
admin.site.register(MailToString)
admin.site.register(TitleTag)


@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        )