from django.core.paginator import Paginator


def pagination(queryset, page_number, get_request):
    paginator = Paginator(queryset, 15)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    prev_url = None
    if page.has_previous():
        get_request['page'] = page.previous_page_number()
        prev_url = '?{}'.format(get_request.urlencode())

    next_url = None
    if page.has_next():
        get_request['page'] = page.next_page_number()
        next_url = '?{}'.format(get_request.urlencode())

    context = {
        'page': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return context
