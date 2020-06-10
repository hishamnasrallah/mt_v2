from django import template
# from CourseApp.models import Course
# from SiteConfiguration.models import AboutUs
from translation.models import SiteLabel

register = template.Library()


@register.simple_tag
def add_as_star_translation():

    label_number = 1
    if SiteLabel.objects.filter(number=label_number):

        label_obj = SiteLabel.objects.get(number=label_number)
        print(label_obj)

    return label_obj

