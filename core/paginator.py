from django.core.paginator import Paginator


def pagination(queryset, page_number):
    PRODUCT_PER_PAGE = 1
    paginator = Paginator(queryset, PRODUCT_PER_PAGE)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page=%s' % page.previous_page_number()
    else:
        prev_url = '' 
    
    if page.has_next():
        next_url = '?page=%s' % page.next_page_number()
    else:
        next_url = '' 

    
    context = {
        'page': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return context