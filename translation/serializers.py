from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from authentication.tokens import VScribeRefreshToken
from translation.doc_mt_translation import translate_ureed, parsing_mxliff
from translation.models import FileTranslation, CustomerInfo
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import json
import encodings




class MTObtainPairSerializer(TokenObtainPairSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        return VScribeRefreshToken.for_user(user)


class MTTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        refresh = VScribeRefreshToken(attrs['refresh'])
        data = {'access': str(refresh.access_token)}
        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass



class TranslateSerializer(serializers.Serializer):
    enu_text = serializers.CharField(required=False, allow_blank=True)
    slug = serializers.CharField(required=False, allow_blank=True, max_length=150)
    user_id = serializers.IntegerField(required=True)
    # source = serializers.CharField(required=True, max_length=3)

    class Meta:
        # model = Message
        fields = [ 'enu_text', 'slug', 'user_id']


class TranslateSerializerExternalUse(serializers.Serializer):
    inputText = serializers.CharField(required=False, allow_blank=True)
    client = serializers.CharField(required=True, max_length=150)
    # user_id = serializers.IntegerField(required=True)
    access_token = serializers.CharField(required=True, max_length=150)
    source = serializers.CharField(required=True, max_length=3)

    class Meta:
        # model = Message
        fields = ['source', 'inputText', 'client', 'access_token']


class TranslateSerializerTMSUse(serializers.Serializer):
    inputText = serializers.CharField(required=False, allow_blank=True)
    client = serializers.CharField(required=True, max_length=150)
    source = serializers.CharField(required=True, max_length=3)
    # user_id = serializers.IntegerField(required=True)
    access_token = serializers.CharField(required=True, max_length=150)

    class Meta:
        # model = Message
        fields = ['inputText', 'client', 'source', 'access_token']


class ClientSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(read_only=True)
    updated_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomerInfo
        fields = '__all__'

class LexicalTranslationSerializer(serializers.Serializer):
    enu_text = serializers.CharField(required=False, allow_blank=True)
    slug = serializers.CharField(required=False, allow_blank=True, max_length=150)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        # model = Message
        fields = ['enu_text', 'slug', 'user_id']

# def reading_uploaded_file(obj):
#
#     print(obj)
#     print(obj.id)
#     print('@@@@@@@@@@@@@@')
#     f = obj.file_en.read()
#
#     print(f)
#     # f.write(content)
#     # f.close()
#     return 2

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTranslation
        fields = ('file_en',)


class TranslateFileSerializer(serializers.ModelSerializer):
    file_en = serializers.ListField(
        child=serializers.FileField(
            max_length=100000,  # length of the file name
            allow_empty_file=False,
            use_url=False
        ),
        write_only=True
    )

    def validate(self, attrs):

        attrs = super(TranslateFileSerializer, self).validate(attrs)  # calling default validation
        file_en = attrs['file_en']
        for i in file_en:
            file_ext = str(i).split('.')[-1]
            if file_ext != 'mxliff':
                raise serializers.ValidationError("you can upload just file ends with extension .mxliff")
        return attrs

    class Meta:
        model = FileTranslation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # many = kwargs.pop('many', True)
        # super(TranslateFileSerializer, self).__init__(many=many, *args, **kwargs)
        user = kwargs['context']['request'].user
        super(TranslateFileSerializer, self).__init__(*args, **kwargs)
        self.fields['client'].queryset = CustomerInfo.objects.filter(employees_accounts=user.id) #User.objects.filter(id=user.id)

    def create(self, validated_data):
        files = validated_data.pop("file_en")

        validated_data['status'] = 'in_progress'
        self.context["file_en"] = self.context['request'].FILES.get("file_en")
        obj = None
        validated_data['client'] = self.fields['client'].queryset.first()
        for file in files:
            obj = FileTranslation.objects.create(file_en=file, **validated_data)
            file_name = str(obj.file_en).split('/')[1]
        # obj = FileTranslation.objects.create(**validated_data)
        # translate_ureed(obj.file_en.read())
            parsing_mxliff.delay(obj.file_en.path, obj.id)
        # parsing_mxliff.delay(obj.file_en.path, obj.id)
        return obj
        # return 2
