from django.http import JsonResponse

def BoolToDictionary(boolean):
    output = {
        'act': boolean
    }

    return output

def returnjson(content):
    return JsonResponse(content, json_dumps_params={'ensure_ascii': False},
                        content_type=u"application/json; charset=utf-8", status=200)