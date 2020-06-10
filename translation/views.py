import requests
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from translation.dictionary_model import Engaradictionary
from translation.permssions import IsOwnerOrReadOnly
from translation.serializers import TranslateSerializer, LexicalTranslationSerializer, TranslateFileSerializer, \
    TranslateSerializerExternalUse, MTTokenRefreshSerializer, MTObtainPairSerializer, TranslateSerializerTMSUse, \
    ClientSerializer
from .resources import TranslationHistoryResource

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, RedirectView, TemplateView, View, \
    ListView

from mt_final.settings import MEDIA_ROOT, SEGMENTATION_ENDPOINT_ar, SEGMENTATION_ENDPOINT_en, MT_ENDPOINT_AR_EN, MT_ENDPOINT_EN_AR
from translation.forms import CustomerForm, TranslationForm, ManageFeatureForm, UserForm, CustomerSubscribeForm
from translation.models import CustomerInfo, ManageFeature, TranslationHistory, TranslationDestinationPref, \
    CustomerSubscription, FileTranslation

import nltk

from django.core.mail import send_mail





@login_required()
def Index(request):

    if request.user.is_superuser:
        return redirect('admin:index')
    if request.user.is_staff and not request.user.is_superuser:
        return redirect('home-staff')
    if not request.user.is_staff and not request.user.is_superuser:
        # print(request.user)
        request_user = request.user
        client_obj = CustomerInfo.objects.filter(Q(user=request_user) |
                                                 Q(employees_accounts=request_user),
                                                 active_ind=True).first()

        return redirect('translate' + '/' + client_obj.slug + '/')


def is_ascii(s):
    return all(ord(c) < 128 or ord(c) == 8217 for c in s)


class TranslationDetailView(DetailView):
    template_name = 'ureed/ureed.html'

    def get(self, request, pk=None, **kwargs):
        user = self.request.user
        star_ind = None
        # print(CustomerInfo.objects.filter(pk=pk))
        trans_history = get_object_or_404(TranslationHistory, pk=pk)
        args = {'to_translate': trans_history.to_translate, 'translated': trans_history.translated,
                'star': trans_history.star_ind}
        return render(request, self.template_name, args)


@login_required()
def mt_translation_view(request, slug=None):
    """
    main translation page
    """


    trans_history = 0
    current_user = None
    if User.objects.filter(pk=request.user.pk):
        current_user = User.objects.get(pk=request.user.pk)
        general_color = None
        button_text_color = None
        if current_user and (CustomerInfo.objects.filter(Q(user=current_user) |
                                                         Q(employees_accounts=current_user),
                                                         active_ind=True,
                                                         slug=slug) or current_user.is_superuser or current_user.is_staff):
            copy_ind = None
            customer_obj = None
            trans_history_id = None
            logo = None
            alt_txt = None
            user_trans_history = None
            files_history = None

            user_trans_history = TranslationHistory.objects.filter(created_by=request.user).order_by('-created_date')[
                                 :10]
            files_history = FileTranslation.objects.filter(created_by=request.user).order_by('-created_date')[
                                 :10]
            if current_user:

                customer_obj = CustomerInfo.objects.filter(
                    Q(user=current_user) | Q(employees_accounts=current_user)).first()
                general_color = customer_obj.general_color
                button_text_color = customer_obj.button_text_color
                if not current_user.is_staff or not current_user.is_superuser:
                    if customer_obj.logo:
                        logo = customer_obj.logo

                if ManageFeature.objects.filter(active_ind=True, customer=customer_obj):
                    features = ManageFeature.objects.get(active_ind=True, customer=customer_obj)
                    copy_ind = features.copy_translated_text_ind
            subscription_to_add_request_counter = CustomerSubscription.objects.filter(active_ind=True,
                                                                                      customer=customer_obj).first()
            if subscription_to_add_request_counter:

                to_translate = ''
                translated = ''
                words_pos = {}
                if request.POST:
                    to_translate = request.POST.get('to_translate')
                    tokens = nltk.word_tokenize(to_translate)
                    words_pos = {}



                    pos_shortcuts = {'CC': 'coordinating conjunction', 'CD': 'cardinal digit', 'DT': 'determiner',
                                     'EX': 'existential there (like: “there is” … think of it like “there exists”)',
                                     'FW': 'foreign word', 'IN': 'preposition/subordinating conjunction',
                                     'JJ': 'adjective ‘big’', 'JJR': 'adjective, comparative ‘bigger’',
                                     'JJS': 'adjective, superlative ‘biggest’', 'LS': 'list marker 1)',
                                     'MD': 'modal could, will', 'NN': 'noun, singular ‘desk’',
                                     'NNS': 'noun plural ‘desks’', 'NNP': 'proper noun, singular ‘Harrison’',
                                     'NNPS': 'proper noun, plural ‘Americans’',
                                     'PDT': 'predeterminer ‘all the kids’',
                                     'POS': 'possessive ending parent’s', 'PRP': 'personal pronoun I, he, she',
                                     'PRP$': 'possessive pronoun my, his, hers', 'RB': 'adverb very, silently,',
                                     'RBR': 'adverb, comparative better', 'RBS': 'adverb, superlative best',
                                     'RP': 'particle give up', 'T': 'O, to go ‘to’ the store.',
                                     'UH': 'interjection, errrrrrrrm', 'VB': 'verb, base form take',
                                     'VBD': 'verb, past tense took',
                                     'VBG': 'verb, gerund/present participle taking',
                                     'VBN': 'verb, past participle taken',
                                     'VBP': 'verb, sing. present, non-3d take',
                                     'VBZ': 'verb, 3rd person sing. present takes', 'WDT': 'wh-determiner which',
                                     'WP': 'wh-pronoun who, what', 'WP$': 'possessive wh-pronoun whose',
                                     'WRB': 'wh-abverb where, when'}
                    for i in tokens:
                        response = Engaradictionary.objects.filter(eng=i.capitalize()).first()
                        if response and (i != 'To' and i != 'to' and i != 'TO'):
                            print(pos_shortcuts[nltk.pos_tag([i])[0][1]])
                            print(response.ara)
                            words_pos[i] = [pos_shortcuts[nltk.pos_tag([i])[0][1]], response.ara]
                    print(words_pos)
                    url = "https://gk0z0bj2hh.execute-api.eu-west-1.amazonaws.com/prod/translation"

                    querystring = {"sentence": to_translate}
                    api_key = None
                    if CustomerInfo.objects.filter(Q(user=request.user) | Q(employees_accounts=request.user)):
                        client_info = CustomerInfo.objects.filter(
                            Q(user=request.user) | Q(employees_accounts=request.user)).first()
                        api_key = client_info.aws_gw_token

                    payload = ""
                    headers = {
                        'x-api-key': api_key,
                        'cache-control': "no-cache"
                    }

                    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
                    if response.status_code == 403:
                        error = 'please contact system administrator to renew your subscription your account'
                        page_title = 'Expiration'
                        error_title = 'Error Code: 403 ---- ' + ' Package Expired'
                        context = {
                            'page_title': page_title,
                            'error_title': error_title,

                            'error': error,

                        }

                        return render(request, 'registration/not_activated.html', context)
                    if 'Arabic_text' in response.json():
                        translated = response.json()['Arabic_text'][0][1]
                    if to_translate:
                        if CustomerInfo.objects.filter(Q(user=request.user) | Q(employees_accounts=request.user)):

                            trans_history = TranslationHistory.objects.create(created_by=current_user,
                                                                              updated_by=current_user,
                                                                              to_translate=to_translate,
                                                                              translated=translated,
                                                                              client=CustomerInfo.objects.filter(
                                                                                  Q(user=request.user) |
                                                                                  Q(
                                                                                      employees_accounts=request.user)).first())
                            trans_history.save()

                            trans_history_id = trans_history.id

                            subscription_to_add_request_counter = CustomerSubscription.objects.filter(active_ind=True,
                                                                                                      customer=customer_obj).first()
                            subscription_to_add_request_counter.number_of_used_requests += 1
                            subscription_to_add_request_counter.save()
                            url = "https://gk0z0bj2hh.execute-api.eu-west-1.amazonaws.com/prod/translation"

                            querystring = {"sentence": to_translate}
                            api_key = None
                            if CustomerInfo.objects.filter(Q(user=request.user) | Q(employees_accounts=request.user)):
                                client_info = CustomerInfo.objects.filter(
                                    Q(user=request.user) | Q(employees_accounts=request.user)).first()
                                api_key = client_info.aws_gw_token

                            payload = ""
                            headers = {
                                'x-api-key': api_key,
                                'cache-control': "no-cache"
                            }

                            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
                        else:
                            trans_history = TranslationHistory.objects.create(created_by=current_user,
                                                                              updated_by=current_user,
                                                                              to_translate=to_translate,
                                                                              translated=translated)
                            trans_history.save()

                    context = {
                        'logo': logo,
                        'POS': words_pos,
                        'alt_txt': alt_txt,
                        'translated': translated,
                        'to_translate': to_translate,
                        'trans_id': trans_history_id,
                        'copy_ind': copy_ind,
                        'translation_history': user_trans_history,
                        'trans_history_id': trans_history.id if trans_history else 0,
                        'files_history': files_history,

                        # 'from_to': translation_way_pref,

                        # 'upload_to_translate': ,
                    }
                    return render(request, 'ureed/ureed.html', context)

                    # return HttpResponse(context)
                elif request.method == 'GET':


                    print('its get request')
                    context = {
                        'logo': logo,
                        'POS': words_pos,
                        'alt_txt': alt_txt,
                        'translated': translated,
                        'to_translate': to_translate,
                        'trans_id': trans_history_id,
                        'copy_ind': copy_ind,
                        'translation_history': user_trans_history,
                        'button_text_color': button_text_color,
                        'general_color': general_color,
                        'slug': slug,
                        'trans_history_id': trans_history.id if trans_history else 0,
                        'files_history': files_history,

                    }
                    return render(request, 'ureed/ureed.html', context)
            else:
                error = 'please contact system administrator to renew your subscription your account'
                page_title = 'Expiration'
                error_title = 'Error Code: 403 ---- ' + ' Package Expired'
                context = {
                    'page_title': page_title,
                    'error_title': error_title,
                    'error': error,
                }
                return render(request, 'registration/not_activated.html', context)
        else:
            error = 'You see this error for one of those reasons (you need to activate your account,' \
                    ' or you are trying to access page that you have not a permission to open).'
            page_title = 'Activation'
            error_title = 'Access rights'
            context = {
                'page_title': page_title,
                'error_title': error_title,
                'error': error,
            }
            return render(request, 'registration/not_activated.html', context)

class LexicalTranslationAPIView(APIView):
    """
    lexical translation api " USED in ureed.html (ajax call)"
    """

    permission_classes = (AllowAny,)
    serializer_class = LexicalTranslationSerializer

    def post(self, request):
        source = request.data['source']
        if source in ['en', 'EN', 'En']:
            if User.objects.filter(pk=request.data['user_id']):
                current_user = User.objects.get(pk=request.data['user_id'])
                if current_user and (CustomerInfo.objects.filter(Q(user=current_user) |
                                                                 Q(employees_accounts=current_user),
                                                                 active_ind=True,
                                                                 slug=request.data['slug']) or current_user.is_superuser or current_user.is_staff):
                    customer_obj = None
                    user_trans_history = TranslationHistory.objects.filter(created_by=current_user).order_by(
                        '-created_date')[:10]
                    # print(user_trans_history)
                    if current_user:
                        customer_obj = CustomerInfo.objects.filter(
                            Q(user=current_user) | Q(employees_accounts=current_user)).first()
                    subscription_to_add_request_counter = CustomerSubscription.objects.filter(active_ind=True,
                                                                                              customer=customer_obj).first()
                    if subscription_to_add_request_counter:

                        to_translate = ''
                        translated = ''
                        # print(request)
                        to_translate = request.data['enu_text']
                        url = SEGMENTATION_ENDPOINT_en  # old

                        # url = "http://localhost:7078/api/segmented_translation"

                        querystring = {"type": 'w', "key": customer_obj.aws_gw_token, "text": to_translate}

                        response = requests.post(url, json=querystring)
                        result = response.json()

                        return Response(result)
                else:
                    return Response({"status": "nothing to show"})

class ProfileLimitPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10


class MTTranslationFileListAPIView(ListAPIView):
    queryset = FileTranslation.objects.all()
    serializer_class = TranslateFileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = ProfileLimitPagination
    parser_classes = (MultiPartParser, FormParser,)
    def get_queryset(self):
        slug = self.kwargs['slug']
        return FileTranslation.objects.filter(client__slug=slug)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

class MTTranslationFileCreateAPIView(CreateAPIView):
    queryset = FileTranslation.objects.all()
    serializer_class = TranslateFileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = ProfileLimitPagination

    def get_queryset(self):
        slug = self.kwargs['slug']
        return FileTranslation.objects.filter(client__slug=slug)

    def perform_create(self, serializer):

        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class MTTranslateFileAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TranslateFileSerializer

    def post(self, request, *args, **kwargs):
        try:

            if User.objects.filter(pk=request.user.id):
                current_user = User.objects.get(pk=request.user.id)
                if current_user and (CustomerInfo.objects.filter(Q(user=current_user) |
                                                                 Q(employees_accounts=current_user),
                                                                 active_ind=True,
                                                                 slug=kwargs['slug']) or current_user.is_superuser or current_user.is_staff):
                    customer_obj = None
                    user_trans_history = TranslationHistory.objects.filter(created_by=current_user).order_by(
                        '-created_date')[:10]
                    if current_user:
                        customer_obj = CustomerInfo.objects.filter(
                            Q(user=current_user) | Q(employees_accounts=current_user)).first()
                    subscription_to_add_request_counter = CustomerSubscription.objects.filter(active_ind=True,
                                                                                              customer=customer_obj).first()
                    if subscription_to_add_request_counter:
                        file_en = ''
                        translated = ''

                        if request.POST:
                            file_obj = request.FILES['file_en']
                            file_name = str(file_obj).split('.')[0]
                            file_en = file_name + '_en'

                            context = {
                                'translated': 'tet',  #results['translation'],
                                'to_translate': file_en,
                            }
                            return Response(context)
                        # end of if request == "POST"
                    else:
                        error = 'please contact system administrator to renew your subscription your account'
                        page_title = 'Expiration'
                        error_title = 'Error Code: 403 ---- ' + ' Package Expired'
                        context = {
                            'page_title': page_title,
                            'error_title': error_title,
                            'error': error,
                        }
                        return Response(context)
                else:
                    error = 'You see this error for one of those reasons (you need to activate your account,' \
                            ' or you are trying to access page that you have not a permission to open).'
                    page_title = 'Activation'
                    error_title = 'Access rights'
                    context = {
                        'page_title': page_title,
                        'error_title': error_title,
                        'error': error,
                    }
                    return Response(context)
        except:
            return Response({'error_message': 'third party issue (segmenter, mt , or integration end points)'})


def translation_star_toggle(request, pk):
    trans_id = pk
    obj = get_object_or_404(TranslationHistory, pk=trans_id)
    if obj:
        if obj.star_ind:
            obj.star_ind = False
        else:
            obj.star_ind = True
        obj.save()
        context = {
            "": obj
        }
        return HttpResponse(context)


# Admin views


class CustomerInfoListView(UserPassesTestMixin, TemplateView):

    def test_func(self):
        return self.request.user.is_staff

    template_name = 'admin/customer_info/customers_list.html'

    def get(self, request, **kwargs):
        user = self.request.user

        customers = CustomerInfo.objects.all()

        args = {'customers': customers, 'current_user': user}
        return render(request, self.template_name, args)


class CustomerInfoCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_staff

    template_name = 'admin/customer_info/customer_info_create.html'

    def get(self, request, **kwargs):
        form = CustomerForm()
        return render(request, self.template_name, {'add_customer': form})

    def post(self, request, **kwargs):

        form = CustomerForm(request.POST)
        post = request.POST.copy()
        employees = request.POST.getlist('employees_accounts')

        print('1')

        if form.is_valid():
            print('22')
            if 'save' in request.POST:
                form.instance.save()
                instance = form.save(commit=False)
                print(instance)
                print(form.instance)
                if 'logo' in request.FILES:
                    print('3')
                    instance.logo = request.FILES['logo']
                instance.save()

                instance.updated_by = self.request.user
                instance.updated_date = timezone.now()
                form.save_m2m()
                return redirect('index')

            elif 'add-another' in request.POST:
                form.save()
                form = CustomerInfoCreateView()
            return redirect('create_customer')
        return render(request, self.template_name, {'add_customer': form})


class CustomerUpdateView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        return self.request.user.is_staff

    template_name = 'admin/customer_info/customer_info_edit.html'
    model = CustomerInfo
    form_class = CustomerForm
    success_url = '/'

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.updated_by = self.request.user
        customer.updated_date = timezone.now()
        customer.save()
        # if form.employees_accounts:
        form.save_m2m()
        return redirect('detail_customer', pk=customer.pk)


class CustomerActivateView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        return self.request.user.is_staff

    model = CustomerInfo


    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.updated_by = self.request.user
        customer.updated_date = timezone.now()
        customer.save()
        # if form.employees_accounts:
        form.save_m2m()
        return redirect('detail_customer', pk=customer.pk)


class CustomerDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        return self.request.user.is_staff

    template_name = 'admin/customer_info/customer_info_detail.html'


    def get(self, request, pk=None, **kwargs):
        user = self.request.user
        features = None
        # print(CustomerInfo.objects.filter(pk=pk))
        customer = CustomerInfo.objects.get(pk=pk)
        if ManageFeature.objects.filter(customer=customer).count() > 0:
            features = ManageFeature.objects.get(customer=customer)
        args = {'customer': customer, 'current_user': user, 'features': features}
        return render(request, self.template_name, args)


class ClientInfoDelete(DeleteView):
    model = CustomerInfo
    success_url = reverse_lazy('home-staff')
    template_name = 'admin/customer_info/confirm_delete.html'


class StaffHome(TemplateView):
    template_name = 'admin/customer_info/home.html'

    def get(self, request, pk=None, **kwargs):
        user = self.request.user
        page = request.GET.get('page', 1)
        customer = CustomerInfo.objects.all().order_by('-created_date')
        paginator = Paginator(customer, 10)
        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)
        args = {'customer': customer, 'current_user': user}
        return render(request, self.template_name, args)


class ManageFeatureCreateView(UserPassesTestMixin, CreateView):

    def test_func(self):
        return self.request.user.is_staff

    template_name = 'admin/customer_info/customer_features_create.html'
    pk_url_kwarg = 'customer'

    def get(self, request, **kwargs):
        form = ManageFeatureForm()
        return render(request, self.template_name, {'add_features': form})

    def post(self, request, **kwargs):
        form = ManageFeatureForm(request.POST)
        # print(self.kwargs['customer'])
        if form.is_valid():
            print('22')
            if 'save' in request.POST:
                form.instance.save()
                instance = form.save(commit=False)
                print(instance)
                print(form.instance)
                if 'logo' in request.FILES:
                    # print('3')
                    instance.logo = request.FILES['logo']
                instance.customer_id = self.kwargs['customer']
                instance.save()

                instance.updated_by = self.request.user
                instance.updated_date = timezone.now()
                form.save_m2m()
                return redirect('index')

            elif 'add-another' in request.POST:
                form.save()
                form = CustomerInfoCreateView()
            return redirect('create_customer')
        return render(request, self.template_name, {'add_features': form})

    def form_valid(self, form):
        customer = get_object_or_404(CustomerInfo, id=self.kwargs['customer'])
        form.instance.customer = customer
        return super(ManageFeatureCreateView, self).form_valid(form)


class ManageFeaturesDetailView(UserPassesTestMixin, DetailView):

    def test_func(self):
        return self.request.user.is_staff

    lookup_field = 'customer'
    template_name = 'admin/customer_info/customer_features_detail.html'


    def get(self, request, customer=None, **kwargs):
        user = self.request.user
        features = None
        customer = ManageFeature.objects.get(pk=customer)
        if CustomerInfo.objects.filter(pk=customer):
            features = ManageFeature.objects.get(customer=customer)
        args = {'current_user': user, 'features': features}
        return render(request, self.template_name, args)


class ManageFeaturesUpdateView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        return self.request.user.is_staff

    template_name = 'admin/customer_info/customer_features_edit.html'
    model = ManageFeature
    form_class = ManageFeatureForm
    success_url = '/'


class CustomerSubscriptionCreateView(UserPassesTestMixin, CreateView):

    def test_func(self):
        return self.request.user.is_staff

    template_name = 'admin/customer_info/customer_subscription_add.html'
    model = CustomerSubscription
    form_class = CustomerSubscribeForm
    success_url = '/'


    def form_valid(self, form):
        subscription = form.save(commit=False)
        subscription.updated_by = self.request.user
        subscription.updated_date = timezone.now()
        subscription.save()


        return redirect('home-staff')


class CustomerSubscriptionsListView(ListView):
    model = TranslationHistory
    template_name = 'admin/customer_info/customer_subscriptions_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'subscriptions'  # Default: object_list
    paginate_by = 10


def create_new_user(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.save()

            registered = True
            return redirect('index')  # render(request, 'index.html')
        else:
            args = {'user_form': user_form, 'registered': registered}
            return render(request, 'registration/signup.html', args)
    else:
        user_form = UserForm()
        # profile_form = UserExtensionForm()
        args = {'user_form': user_form, 'registered': registered}
        return render(request, 'registration/signup.html', args)


class TranslationsListView(ListView):
    model = TranslationHistory
    queryset = TranslationHistory.objects.all().order_by('-created_date')
    template_name = 'admin/translation/translations_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'translations'  # Default: object_list
    paginate_by = 10



def export_translation_data(request):
    translations_resource = TranslationHistoryResource()

    dataset = translations_resource.export()

    response = HttpResponse(dataset.csv, content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="translations.csv"'
    return response



class MTTokenObtainPairView(TokenObtainPairView):
    serializer_class = MTObtainPairSerializer


class MTTokenRefreshView(TokenRefreshView):
    serializer_class = MTTokenRefreshSerializer


class MTTranslateAPIViewTMSlUse(APIView):
    permission_classes = [AllowAny,]
    serializer_class = TranslateSerializerTMSUse

    def post(self, request):

        try:
            _source = request.data['source']
            access_token = request.data['access_token']
            slug = request.data['client']
            input_text = request.data['inputText']
            # print(get_object_or_404(CustomerInfo, slug=slug))
            client = CustomerInfo.objects.filter(slug=slug).first()
            print(access_token, slug, input_text, client)
            if not client:
                return Response({'error': 'client does not exist'})
            else:
                try:
                    correct_access_token = client.access_token
                    if access_token != correct_access_token:
                        return Response({'error': 'Access token is wrong'})
                    elif access_token == correct_access_token and not client.access_token_active_ind:
                        return Response({'error': 'Access token is not active'})
                except:
                    return Response({'error': 'there is no available access token.'})

            print(client.id)

            customer_obj = None

            customer_obj = client
            subscription_to_add_request_counter = CustomerSubscription.objects.filter(active_ind=True,
                                                                                      customer=customer_obj).first()
            if subscription_to_add_request_counter:
                to_translate = ''
                translated = ''
                print(request.method)
                to_translate = input_text
                # TODO:// the following code should be for MT endpoint direct

##############################################################
                # # url = "http://localhost:5022/api/segmented_translation"  # new
                # url = SEGMENTATION_ENDPOINT  # old
                # # url = "http://localhost:7078/api/segmented_translation"
                # querystring = {"type": 's', "key": customer_obj.aws_gw_token, "text": to_translate}
                # response = requests.request("POST", url, json=querystring)
####################################################################
                ar = False
                en = False
                if _source in ['ara', 'ar', 'ARA', 'AR']:
                    mt_url = MT_ENDPOINT_AR_EN
                    ar = True
                    headers = {
                        'x-api-key': customer_obj.aws_gw_token,
                        'cache-control': 'no-cache',
                    }
                    querystring = {"sentence": to_translate}
                    response = requests.get(url=mt_url, params=querystring, headers=headers)
                    print(response.json().get("target_text")[0][1])

                elif _source in ['enu', 'en', 'ENU', 'EN']:
                    mt_url = MT_ENDPOINT_EN_AR
                    en = True
                    headers = {
                        'x-api-key': customer_obj.aws_gw_token,
                        'cache-control': 'no-cache',
                    }
                    querystring = {"sentence": to_translate}
                    response = requests.get(url=mt_url, params=querystring, headers=headers)

                    print(response.json().get("Arabic_text")[0][1])

                else:
                    error = "wrong source language it should be one of these " \
                            "['ara', 'ar', 'ARA', 'AR', 'enu', 'en', 'ENU', 'EN']"
                    page_title = 'Wrong source language'
                    error_title = 'Error Code: 403 ---- ' + ' Wrong selected language'
                    context = {
                        'page_title': page_title,
                        'error_title': error_title,
                        'error': error,
                    }
                    return Response(context)



                if response.status_code == 403:
                    error = 'please contact system administrator to renew your subscription your account'
                    page_title = 'Expiration'
                    error_title = 'Error Code: 403 ---- ' + ' Package Expired'
                    context = {
                        'page_title': page_title,
                        'error_title': error_title,
                        'error': error,
                    }
                    return Response(context)
                print(response)

                results = response.json()
                print(results)
                if results:

                    if ar:
                        if CustomerInfo.objects.filter(slug=slug):
                            trans_history = TranslationHistory.objects.create(created_by=None,
                                                                              updated_by=None,
                                                                              to_translate=to_translate,
                                                                              translated=results['target_text'][0][1],
                                                                              client=CustomerInfo.objects.filter(
                                                                                  slug=slug).first())
                            trans_history.save()
                        context = {
                            'originalText': to_translate,
                            'translatedText': results['target_text'][0][1],
                        }
                    elif en:
                        if CustomerInfo.objects.filter(slug=slug):
                            trans_history = TranslationHistory.objects.create(created_by=None,
                                                                              updated_by=None,
                                                                              to_translate=to_translate,
                                                                              translated=results['Arabic_text'][0][1],
                                                                              client=CustomerInfo.objects.filter(
                                                                                  slug=slug).first())
                            trans_history.save()
                        context = {
                            'originalText': to_translate,
                            'translatedText': results['Arabic_text'][0][1],
                        }
                return Response(context)

            else:
                error = 'please contact system administrator to renew your subscription your account'
                page_title = 'Expiration'
                error_title = 'Error Code: 403 ---- ' + ' Package Expired'
                context = {
                    'page_title': page_title,
                    'error_title': error_title,
                    'error': error,
                }
                return Response(context)
        except:
            return Response({
                    'page_title': "Third party error",
                    'error_title': 'Error Code: 403 ---- ' + ' external error error',
                    'error': 'something went wrong'})


class CreateClientAPIView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ClientSerializer




class MTTranslateAPIView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = TranslateSerializerTMSUse

    def post(self, request):

        try:
            _source = request.data.get('source', None)
            slug = request.data.get('slug', None)
            user_id = request.data.get('user_id', None)
            access_token = get_object_or_404(CustomerInfo, slug=slug).access_token
            #// TODO: the following line should be remove and add a query for that
            # access_token = request.data.get('access_token', None)
            # slug = request.data.get('client', None)
            input_text = request.data.get('inputText', None)
            # print(get_object_or_404(CustomerInfo, slug=slug))
            client = CustomerInfo.objects.filter(slug=slug).first()
            print(access_token, slug, input_text, client)
            if not client:
                return Response({'error': 'client does not exist'})
            else:
                try:
                    correct_access_token = client.access_token
                    if access_token != correct_access_token:
                        return Response({'error': 'Access token is wrong'})
                    elif access_token == correct_access_token and not client.access_token_active_ind:
                        return Response({'error': 'Access token is not active'})
                except:
                    return Response({'error': 'there is no available access token.'})

            customer_obj = None

            customer_obj = client
            subscription_to_add_request_counter = CustomerSubscription.objects.filter(active_ind=True,
                                                                                      customer=customer_obj).first()
            if subscription_to_add_request_counter:
                to_translate = input_text
                ar = False
                en = False
                if _source in ['ara', 'ar', 'ARA', 'AR']:
                    mt_url = SEGMENTATION_ENDPOINT_ar

                    ar = True
                    querystring = {"type": 's', "key": customer_obj.aws_gw_token, "text": to_translate}
                    response = requests.request("POST", mt_url, json=querystring)

                    print(response.json().get("translation"))

                elif _source in ['enu', 'en', 'ENU', 'EN']:
                    mt_url = SEGMENTATION_ENDPOINT_en
                    en = True
                    querystring = {"type": 's', "key": customer_obj.aws_gw_token, "text": to_translate}

                    response = requests.request("POST", mt_url, json=querystring)

                    print(response.json().get("translation"))

                else:
                    error = "wrong source language it should be one of these " \
                            "['ara', 'ar', 'ARA', 'AR', 'enu', 'en', 'ENU', 'EN']"
                    page_title = 'Wrong source language'
                    error_title = 'Error Code: 403 ---- ' + ' Wrong selected language'
                    context = {
                        'page_title': page_title,
                        'error_title': error_title,
                        'error': error,
                    }
                    return Response(context)


                if response.status_code == 403:
                    error = 'please contact system administrator to renew your subscription your account'
                    page_title = 'Expiration'
                    error_title = 'Error Code: 403 ---- ' + ' Package Expired'
                    context = {
                        'page_title': page_title,
                        'error_title': error_title,
                        'error': error,
                    }
                    return Response(context)

                results = response.json()
                if results:

                    if ar:
                        if CustomerInfo.objects.filter(slug=slug):
                            trans_history = TranslationHistory.objects.create(created_by_id=user_id,
                                                                              updated_by_id=user_id,
                                                                              to_translate=to_translate,
                                                                              translated=results['translation'],
                                                                              client=CustomerInfo.objects.filter(
                                                                                  slug=slug).first())
                            trans_history.save()
                        context = {
                            'originalText': to_translate,
                            'translatedText': results['translation'],
                        }
                    elif en:
                        if CustomerInfo.objects.filter(slug=slug):
                            trans_history = TranslationHistory.objects.create(created_by_id=user_id,
                                                                              updated_by_id=user_id,
                                                                              to_translate=to_translate,
                                                                              translated=results['translation'],
                                                                              client=CustomerInfo.objects.filter(
                                                                                  slug=slug).first())
                            trans_history.save()
                        context = {
                            'originalText': to_translate,
                            'translatedText': results['translation'],
                        }
                subscription_to_add_request_counter.number_of_used_requests += 1
                subscription_to_add_request_counter.save()
                return Response(context)

            else:
                error = 'please contact system administrator to renew your subscription your account'
                page_title = 'Expiration'
                error_title = 'Error Code: 403 ---- ' + ' Package Expired'
                context = {
                    'page_title': page_title,
                    'error_title': error_title,
                    'error': error,
                }
                return Response(context)
        except:
            return Response({
                    'page_title': "Third party error",
                    'error_title': 'Error Code: 403 ---- ' + ' external error error',
                    'error': 'something went wrong'})
