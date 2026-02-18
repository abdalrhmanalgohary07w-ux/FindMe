from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "name": "FindMe API",
        "version": "1.0",
        "status": "running",
        "endpoints": {
            "admin": "/admin/",
            "missing_persons": "/api/missing-persons/",
            "search": "/api/missing-persons/search-by-image/"
        }
    })
