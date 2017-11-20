from django.shortcuts import render_to_response,render
from django.template import RequestContext
from partner.models import Distributor, Retailer

def index(request):
    # Generate counts of some of the main objects
    num_distributors = Distributor.objects.all().count()
    num_retailers = Retailer.objects.all().count()
    run_migations()

    return render(
        request,
        'home/index.html',
        context={'num_distributors': num_distributors, 'num_retailers': num_retailers},
    )


def run_migations():
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token

    for user in User.objects.all():
        Token.objects.get_or_create(user=user)
