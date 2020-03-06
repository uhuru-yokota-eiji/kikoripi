from django.http.response import JsonResponse


def index(request):
    print("index")
    response = request.GET
    return JsonResponse(response)
