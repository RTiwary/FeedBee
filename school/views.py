from django.http import HttpResponse
import os
import json

def microsoftAuth(request):
    data = {
        "associatedApplications": [
            {
                "applicationId": os.environ['applicationID']
            }
        ]
    }
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')
