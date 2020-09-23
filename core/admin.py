from django.contrib import admin
from core.models import MailFromString, MailToString, TitleTag, Index, Slide, Banner, InstagramPhotos


admin.site.register(MailFromString)
admin.site.register(MailToString)
admin.site.register(TitleTag)
admin.site.register(Index)
admin.site.register(Slide)
admin.site.register(Banner)
admin.site.register(InstagramPhotos)
