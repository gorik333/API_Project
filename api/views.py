import json

from .models import UserRequest, UserIP
from .forms import TestForm
from .utils import save_request
from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_requests(request):
    requests = UserRequest.objects.filter(ip__ip=get_client_ip(request)).values('email', 'password',
                                                                                'first_name', 'last_name')
    output = json.dumps({'requests': list(requests)}, indent=4)
    content = {
        'json_response': output,
        'status': 'HTTP 200 OK',
    }
    return render(request, 'my_form.html', content, status=200)


# @csrf_exempt
def post_requests(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_ip, created = UserIP.objects.get_or_create(ip=get_client_ip(request))
            save_request(user_ip, data)

            output = json.dumps(data, indent=4)
            content = {
                'form': form,
                'json_response': output,
                'status': 'HTTP 201 Created',
            }
            return render(request, 'my_form.html', content, status=201)
        else:
            output = json.dumps(dict(form.errors.items()), indent=6)
            content = {
                'form': form,
                'json_response': output,
                'status': 'HTTP 400 Bad Request',

            }
            return render(request, 'my_form.html', content, status=400)

    else:
        form = TestForm()

    return render(request, 'my_form.html', {'form': form})
