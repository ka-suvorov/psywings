from django.shortcuts import render


def view_landing(request):
    return render(request, 'pages/index.html', {})