from pages.models import Page
from contacts.models import Social, ContactInfo
from pages.models import Page
from core.models import Index, TitleTag
from products.models import Category
from users.forms import LoginForm, RegisterForm


def context_info(request):
    socials = Social.objects.all()
    drop_pages = Page.objects.filter(is_active=True, action='dropdown')
    top_menu = Page.objects.filter(is_active=True, parent=None)
    whatsapp = Social.objects.filter(name__icontains='whatsapp').first()
    categories = Category.objects.all()
    seo_titles = TitleTag.objects.filter(url=request.path).first()

    try:
        index = Index.objects.first()
    except:
        index = Index.objects.none()

    try:
        contact_info = ContactInfo.objects.first()
    except:
        contact_info = ContactInfo.objects.none()

    login_form = LoginForm()
    register_form = RegisterForm()

    context = {
        'login_form': login_form,
        'register_form': register_form,
        'socials': socials,
        'drop_pages': drop_pages,
        'contact_info': contact_info,
        'whatsapp': whatsapp,
        'top_menu': top_menu,
        'index': index,
        'categories': categories,
        'seo_titles': seo_titles,
    }
    return context