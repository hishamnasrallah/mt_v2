from django.contrib.auth.models import AnonymousUser
from django.db.models import Q

from translation.models import CustomerInfo


def client_logo(request):
    if hasattr(request, 'user'):
        ureed_logo = "/static/img/ureed_logo.png"

        user = request.user
        if user == AnonymousUser() or user.is_staff or user.is_superuser:

            return {
                'logo': ureed_logo,
            }

        else:
            customers = CustomerInfo.objects.filter(Q(user=user) | Q(employees_accounts=user), active_ind=True).first()

            if customers:

                if customers.logo:
                    logo = customers.logo
                    return {
                        'logo': logo,
                    }
                else:
                    return {
                        'logo': ureed_logo,
                    }


