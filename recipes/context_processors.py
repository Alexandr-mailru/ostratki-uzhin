def site_settings(request):
    return {
        'site_name': 'Остатки → Ужин',
        'current_url': request.resolver_match.url_name if request.resolver_match else '',
    }
