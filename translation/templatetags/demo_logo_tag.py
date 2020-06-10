from django import template
# from CourseApp.models import Course
# from SiteConfiguration.models import AboutUs
from translation.models import CustomerInfo

register = template.Library()



@register.simple_tag
def logo_based_on_current_user():

    user = 1
    if CustomerInfo.objects.filter(user=user):

        demo_obj = CustomerInfo.objects.get(user=user)
        print(demo_obj)

    return 2

