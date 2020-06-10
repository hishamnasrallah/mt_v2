from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField

from translation.models import CustomerInfo, TranslationHistory, ManageFeature, Subscription, CustomerSubscription


class CustomerForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(CustomerForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomerInfo
        fields = '__all__'
        exclude = ('created_by', 'updated_by')
    # def clean(self):
    # def clean(self):
    #
    #     cleaned_data = self.cleaned_data
    #     print('fdsfdsfdsf')
    #     print(cleaned_data['name'])
    #     if cleaned_data['customer_type'] == "PRSN":
    #         # cleaned_data.update('number_of_employee')
    #         cleaned_data['number_of_employees'] = 0
    #         cleaned_data.pop('employees_accounts')
    #         # cleaned_data['employees_accounts'] = None
    #
    #         # // TODO: remove old employess in update
    #         #     if CustomerInfo.objects.filter(pk= self.instance.pk):
    #         #         employees_accounts = self.instance.employees_accounts
    #         #
    #         #         x = CustomerInfo.objects.get(pk= self.instance.pk)
    #         #         x.employees_accounts.remove()
    #
    #         # employees_accounts = self.instance.employees_accounts
    #         # self.instance.employees_accounts.remove(employees_accounts)
    #     # print(cleaned_data['employees_accounts'])
    #     # print(cleaned_data['employees_accounts'].count( ))
    #     if CustomerInfo.objects.filter(pk=self.instance.pk):
    #         x = CustomerInfo.objects.get(pk=self.instance.pk)
        # existing_emp_no = x.employees_accounts.count()
        # new_emp = 0
        # if cleaned_data['employees_accounts'].exist():
        #     print('counted')
        #     new_emp = cleaned_data['employees_accounts'].count()
        # print(existing_emp_no + new_emp)

        # print(cleaned_data['employees_accounts'].count())

        # print(cleaned_data['employees_accounts'])
        # if cleaned_data['number_of_employees'] < cleaned_data['employees_accounts'].count():
        #     print(' its less')
        #
        # if self._errors:
        #     self.data['password'] = 'abc'
        #     raise forms.ValidationError("You have failed validation!")
        # else:
        #     return cleaned_data
            # def clean_customer_type(instance):
    #     if instance.customer_type == "PRSN":
    #         instance.number_of_employees = 0
    #         instance.employees_accounts = None
    #
    # def clean_number_of_employees(self):
    #     if self.number_of_employees < self.employees_accounts.count():
    #         raise ValidationError("errrrrrrrrr")
    # # def clean_employees_accounts(self):


class ManageFeatureForm(forms.ModelForm):

    class Meta:
        model = ManageFeature
        fields = '__all__'
        exclude = ('created_by', 'updated_by')


class SubscriptionsSelect2Form(forms.Form):
    subscriptions = ModelMultipleChoiceField(queryset=Subscription.objects.all())


class CustomerSubscribeForm(forms.ModelForm):

    class Meta:
        model = CustomerSubscription
        fields = '__all__'
        exclude = ('created_by', 'updated_by')



class TranslationForm(forms.ModelForm):
    class Meta:
        model = TranslationHistory
        fields = '__all__'


class MyForm(forms.Form):
    things = ModelMultipleChoiceField(queryset=User.objects.all())

class UserForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = User
        help_texts = {'username': ''}
        fields = (
            'username',
            'first_name',
            'last_name',
            # 'email',
            'password1',
            'password2'
        )

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password1", )
        confirm_password = cleaned_data.get("password2", )
        if password != confirm_password:
            raise forms.ValidationError(
                "password and Confirm password does not match"
            )


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)