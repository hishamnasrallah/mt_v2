from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models


# from django.dispatch import receiver
# Create your models here.
from django.urls import reverse
from colorful.fields import RGBColorField
from django.utils.text import slugify

# from Global_Functions.random_key import randomString

import random
import string




class TranslationDestinationPref(models.Model):
    translation_way = (('1', 'English/Arabic'), ('2', 'Arabic/English'))

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='main user')
    translation_way = models.CharField(max_length=1, choices=translation_way, verbose_name='Translation from/to',
                                       default="1")


class CustomerInfo(models.Model):
    CUSTOMER_TYPE_CHOICES = (('PRSN', 'Personal'), ('COMP', 'Company'))

    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350)
    logo = models.ImageField(upload_to='images/', max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                             verbose_name='Manager user of this client')
    customer_type = models.CharField(max_length=4, choices=CUSTOMER_TYPE_CHOICES, verbose_name='Type', default="COMP")
    number_of_employees = models.IntegerField(null=True, blank=True,
                                              verbose_name='number of accounts can use the application')
    employees_accounts = models.ManyToManyField(User, related_name='employees_accounts', verbose_name='Employees',
                                                blank=True)
    general_color = RGBColorField(null=True, blank=True, default='#0ad0ba')
    button_text_color = RGBColorField(null=True, blank=True, default='#ffffff')
    access_token = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='Access Token')
    access_token_active_ind = models.BooleanField(default=True)
    aws_gw_token = models.CharField(max_length=100, null=True, blank=True, verbose_name='AWS GW Token')

    active_ind = models.BooleanField(default=True, verbose_name='active indicator')

    created_by = models.ForeignKey(User, related_name='CustomerInfo_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, verbose_name='last updated date')
    updated_by = models.ForeignKey(to=User, null=True, related_name='CustomerInfo_updated_by',
                                   verbose_name='last updated by',
                                   blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.pk:
            access_token_key = self.randomString()
            is_there_same_token = CustomerInfo.objects.filter(access_token__in=access_token_key)
            while is_there_same_token:
                access_token_key = self.randomString()
                is_there_same_token = CustomerInfo.objects.filter(access_token__in=access_token_key)

            self.access_token = access_token_key
        return super(CustomerInfo, self).save(*args, **kwargs)

    def randomString(self, stringLength=100):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        _string_key = ''.join(random.choice(letters) for i in range(stringLength))
        return _string_key

class Subscription(models.Model):
    number_of_request = models.IntegerField(null=True, blank=True)

    created_by = models.ForeignKey(User, related_name='Subscription_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, verbose_name='last updated date')
    updated_by = models.ForeignKey(to=User, null=True, related_name='Subscription_updated_by',
                                   verbose_name='last updated by',
                                   blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.number_of_request) + ' ' + 'requests'


class CustomerSubscription(models.Model):
    customer = models.ForeignKey(CustomerInfo, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Client')
    subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.DO_NOTHING)
    number_of_used_requests = models.IntegerField(default=0, null=True, blank=True, verbose_name='Number of used requests')
    active_ind = models.BooleanField(default=True, verbose_name='Active')
    created_by = models.ForeignKey(User, related_name='customer_subscription_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, verbose_name='last updated date')
    updated_by = models.ForeignKey(to=User, null=True, related_name='customer_subscription_updated_by',
                                   verbose_name='last updated by',
                                   blank=True, on_delete=models.DO_NOTHING)


    def get_some_needed_data_for_save(self):
        customer_info_obj = CustomerInfo.objects.get(pk=self.customer.pk)
        active_subscription = customer_info_obj.subscription_to_use
        subscription_requests = active_subscription.subscription.number_of_request
        number_of_used_requests = active_subscription.number_of_used_requests
        available_requests = subscription_requests - number_of_used_requests
        last_subscription = CustomerSubscription.objects.filter(customer=customer_info_obj,
                                                                last_subscription_ind=True).first()
        new_order_num = last_subscription.ordering + 1
        data_dict = {'customer_info_obj': customer_info_obj,
                     'active_subscription': active_subscription,
                     'subscription_requests': subscription_requests,
                     'number_of_used_requests': number_of_used_requests,
                     'available_requests': available_requests,
                     'last_subscription': last_subscription,
                     'new_order_num': new_order_num}
        return data_dict

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            CustomerSubscription.objects.filter(customer=self.customer).update(active_ind=False)
            self.active_ind = True
        elif self.pk:
            if self.number_of_used_requests >= self.subscription.number_of_request:
                # print('you finished your package')
                self.active_ind = False

        return super(CustomerSubscription, self).save()


class SiteLabel(models.Model):
    # label = models.CharField(max_length=500, null=True, blank=True, verbose_name='Label')
    label = RichTextField(null=True, blank=True)

    description = models.CharField(max_length=100, null=True, blank=True, verbose_name='Description')
    number = models.IntegerField(default=0, null=True, blank=True, verbose_name='Label Number')
    active_ind = models.BooleanField(default=True, verbose_name='Active')

    created_by = models.ForeignKey(User, related_name='site_label_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, verbose_name='last updated date')
    updated_by = models.ForeignKey(to=User, null=True, related_name='site_label_updated_by',
                                   verbose_name='last updated by',
                                   blank=True, on_delete=models.DO_NOTHING)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.number:
            max_num = SiteLabel.objects.all().order_by('-number').first().exclude(self.id)

            print(max_num.number)
            number_to_set = max_num.number + 1
            print(number_to_set)
            self.number = number_to_set

        return super(SiteLabel, self).save()

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     # data_before_save = self.get_some_needed_data_for_save()
    #
    #     customer_info_obj = CustomerInfo.objects.get(pk=self.customer.pk)
    #     active_subscription = customer_info_obj.subscription_to_use
    #
    #     subscription_requests = active_subscription.subscription.number_of_request
    #     number_of_used_requests = active_subscription.number_of_used_requests
    #     available_requests = subscription_requests - number_of_used_requests
    #     last_subscription = CustomerSubscription.objects.filter(customer=customer_info_obj,
    #                                                             last_subscription_ind=True).first()
    #     new_order_num = last_subscription.ordering + 1
    #
    #     if not self.pk:
    #
    #         if CustomerSubscription.objects.filter(customer=self.customer) and not self.pk:
    #             CustomerSubscription.objects.filter(customer=self.customer).update(last_subscription_ind=False)
    #             print('success update last_subscription_ind to False')
    #             self.last_subscription_ind = True
    #             self.active_ind = True
    #         super(CustomerSubscription, self).save()
    #
    #     if not customer_info_obj.subscription_to_use:
    #         customer_info_obj.subscription_to_use = self
    #         customer_info_obj.save()
    #
    #     # elif available_requests == 0:
    #     #     print('avail ==== 0')
    #     #     active_subscription.active_ind = False
    #     #     active_subscription.save()
    #     #     customer_info_obj.subscription_to_use = CustomerSubscription.objects.order_by('ordering').filter(customer=self.customer).first()
    #     #     customer_info_obj.save()
    #
    #         print('its update')
    #     return True



    # def __str__(self):
    #     print(self.subscription)
    #     return str(self.ordering) + ' | ' + self.customer.name + ' | ' + str(self.subscription.number_of_request) + ' Requests'

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     # ValidationError = 'Footer columns values summation should be exactly 12'
    #     if self.customer_type == 'PRSN':
    #         accounts = None
    #         # if self.employees_accounts:
    #         #     print('hisham')
    #         #     self.employees_accounts = None
    #         # //TODO: remove all many to may records if self.type = person
    #
    #             # accounts = self.employees_accounts
    #             # print(self.employees_accounts)
    #             # print(accounts)
    #             # users = User.objects.all()
    #             # self.employees_accounts.remove(users)
    #             # for i in self.employees_accounts:
    #             #     i.clear()
    #         self.number_of_employees = 1
    #     # else:
    #     #     obj = ManageAppearance.objects.filter(active_ind=True).exclude(pk=self.pk)
    #     #     if obj and self.active_ind:
    #     #         obj.update(active_ind=False)
    #     #
    #     #     elif not obj and not self.active_ind:
    #     #         self.active_ind = True
    #         super(CustomerInfo, self).save()


class ManageFeature(models.Model):
    # name = models.CharField(max_length=150)

    customer = models.ForeignKey(CustomerInfo, null=True, blank=True, on_delete=models.CASCADE)
    upload_to_translate_ind = models.BooleanField(default=True, verbose_name='upload to translate text')
    copy_translated_text_ind = models.BooleanField(default=True, verbose_name='copy translated text')

    # footer = models.BooleanField(default=True)
    # logo = models.BooleanField(default=True)
    # logo_image = models.ImageField(upload_to='site_configuration/logo/', null=True, blank=True)
    # register = models.BooleanField(default=False)
    # login = models.BooleanField(default=False)

    active_ind = models.BooleanField(default=True)

    created_by = models.ForeignKey(User, related_name='manage_features_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, verbose_name='last updated date')
    updated_by = models.ForeignKey(to=User, null=True, related_name='manage_features_updated_by', blank=True,
                                   verbose_name='last updated by', on_delete=models.DO_NOTHING)


class TranslationHistory(models.Model):
    to_translate = models.TextField()
    translated = models.TextField()
    file_to_translate = models.FileField(upload_to='uploads_file_to_translate/%Y/%m/%d/', null=True)
    client = models.ForeignKey(to='CustomerInfo', blank=True, null=True, related_name='translation_client',
                               on_delete=models.DO_NOTHING)
    star_ind = models.BooleanField(default=False, verbose_name='stared translation')
    created_by = models.ForeignKey(User, related_name='translation_history_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, verbose_name='last updated date')
    updated_by = models.ForeignKey(to=User, null=True, related_name='translation_history_updated_by', blank=True,
                                   verbose_name='last updated by', on_delete=models.DO_NOTHING)

    def get_absolute_url(self):
        return reverse("translation_detail", kwargs={"pk": self.id})

# class Test1(models.Model):
#     name = models.CharField(max_length=100)
#     users = models.ManyToManyField(to='User')

class FileTranslation(models.Model):

    STATUS_CHOICES = (("not_started", "Not Started"), ("in_progress", "In Progress"), ("completed", "Completed"))
    file_en = models.FileField(upload_to='translation_docs/', null=True, blank=True)
    # file_ar = models.FileField(upload_to='translation_docs/', null=True, blank=True)
    client = models.ForeignKey(to='CustomerInfo', blank=True, null=True, related_name='file_translation_client',
                               on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=30, null=True, blank=True, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(User, related_name='file_translation_created_by', blank=True, null=True,
                                   on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, verbose_name='last updated date')
    updated_by = models.ForeignKey(to=User, null=True, related_name='file_translation_updated_by', blank=True,
                                   verbose_name='last updated by', on_delete=models.DO_NOTHING)

