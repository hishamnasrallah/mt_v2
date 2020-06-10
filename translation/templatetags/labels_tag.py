from django import template
# from CourseApp.models import Course
# from SiteConfiguration.models import AboutUs
from translation.models import SiteLabel

register = template.Library()


@register.simple_tag
def login_page_label():

    label_number = 1
    label_obj = None
    if SiteLabel.objects.filter(number=label_number):

        label_obj = SiteLabel.objects.get(number=label_number)
        print(label_obj)

    return label_obj


@register.simple_tag
def translation_page_label():

    label_number = 2
    label_obj = None
    if SiteLabel.objects.filter(number=label_number):

        label_obj = SiteLabel.objects.get(number=label_number)
        print(label_obj)

    return label_obj

