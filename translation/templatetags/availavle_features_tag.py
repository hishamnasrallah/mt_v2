from django import template
# from CourseApp.models import Course
# from SiteConfiguration.models import AboutUs
# from django.template import context

from translation.models import ManageFeature

register = template.Library()


@register.inclusion_tag('ureed/ureed.html', takes_context=True)
def list_of_features(context):
    # request = context['request']
    # user = 1
    user = None
    print('test')
    # print(context['request'])
    if ManageFeature.objects.filter(customer=user):

        demo_obj = ManageFeature.objects.get(customer=user)
        print(demo_obj)

    return 2

