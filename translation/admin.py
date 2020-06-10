from django.contrib import admin

# Register your models here.
from Global_Functions.admin_panel import AfterSave
from translation.models import CustomerInfo, ManageFeature, TranslationHistory, TranslationDestinationPref, \
    Subscription, CustomerSubscription, SiteLabel, FileTranslation

def generate_access_token_admin_action(modeladmin, request, queryset):
    for client in queryset:

        customer_obj = CustomerInfo()
        access_token_key = customer_obj.randomString(100)
        is_there_same_token = CustomerInfo.objects.filter(access_token__in=access_token_key)
        while is_there_same_token:
            access_token_key = customer_obj.randomString()
            is_there_satme_token = CustomerInfo.objects.filter(access_token__in=access_token_key)

        client.access_token = access_token_key
        client.save()

generate_access_token_admin_action.short_description = 'Generate access token'


class RequestedDemoAdmin(admin.ModelAdmin):

    # add_form_template = 'admin/customer_info/customer_info_create.html'

    search_fields = ['user', 'id', 'name']
    # list_filter = ('tags', 'type')
    list_display = ('id', 'name', 'user', 'active_ind', 'created_date', 'created_by', 'updated_date', 'updated_by')
    actions = [generate_access_token_admin_action, ]  # <-- Add the list action function here

    raw_id_fields = ['user', 'updated_by', 'created_by']

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)


class ManageFeaturesAdmin(admin.ModelAdmin):

    search_fields = ['user', 'id', 'customer']
    # list_filter = ('tags', 'type')
    list_display = ('id', 'customer', 'active_ind', 'created_date', 'created_by', 'updated_date', 'updated_by')

    raw_id_fields = ['customer', 'updated_by', 'created_by']

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)


class TranslationHistoryAdmin(admin.ModelAdmin):
    search_fields = ['created_by__username', 'id', 'to_translate']
    list_filter = ('client', 'created_by__username')
    list_display = ('id', 'to_translate', 'translated', 'created_date', 'created_by', 'updated_date', 'updated_by')

    raw_id_fields = ['updated_by', 'created_by']

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)


class CustomerSubscriptionAdmin(admin.ModelAdmin):
    search_fields = ['customer__name', 'id', 'subscription__number_of_request']
    list_display = ('id', 'customer', 'subscription', 'created_date', 'created_by', 'updated_date', 'updated_by')
    raw_id_fields = ['updated_by', 'created_by', 'customer', 'subscription']

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)


class SiteLabelAdmin(admin.ModelAdmin):
    search_fields = ['description', 'id', 'label', 'number']
    list_display = ('id', 'number', 'description', 'active_ind', 'created_date', 'created_by', 'updated_date', 'updated_by')
    raw_id_fields = ['updated_by', 'created_by']

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)


admin.site.register(CustomerInfo, RequestedDemoAdmin)
admin.site.register(ManageFeature, ManageFeaturesAdmin)
admin.site.register(TranslationHistory, TranslationHistoryAdmin)
admin.site.register(TranslationDestinationPref)
admin.site.register(Subscription)
admin.site.register(CustomerSubscription, CustomerSubscriptionAdmin)
admin.site.register(SiteLabel, SiteLabelAdmin)
admin.site.register(FileTranslation)

