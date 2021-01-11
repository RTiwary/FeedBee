from django.http import JsonResponse
import os

def microsoftAuth(request):
    return JsonResponse(
        {
            "associatedApplications": [
                {
                    "applicationId": os.environ['applicationID']
                }
            ]
        }
    )