# Generated by Django 2.2.1 on 2020-06-05 09:51

import ckeditor.fields
import colorful.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Engaradictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eng', models.CharField(blank=True, max_length=28, null=True)),
                ('ara', models.CharField(blank=True, max_length=120, null=True)),
            ],
            options={
                'db_table': '_engaradictionary',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('slug', models.SlugField(max_length=350)),
                ('logo', models.ImageField(blank=True, max_length=200, null=True, upload_to='images/')),
                ('customer_type', models.CharField(choices=[('PRSN', 'Personal'), ('COMP', 'Company')], default='COMP', max_length=4, verbose_name='Type')),
                ('number_of_employees', models.IntegerField(blank=True, null=True, verbose_name='number of accounts can use the application')),
                ('general_color', colorful.fields.RGBColorField(blank=True, default='#0ad0ba', null=True)),
                ('button_text_color', colorful.fields.RGBColorField(blank=True, default='#ffffff', null=True)),
                ('access_token', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Access Token')),
                ('access_token_active_ind', models.BooleanField(default=True)),
                ('aws_gw_token', models.CharField(blank=True, max_length=100, null=True, verbose_name='AWS GW Token')),
                ('active_ind', models.BooleanField(default=True, verbose_name='active indicator')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='last updated date')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='CustomerInfo_created_by', to=settings.AUTH_USER_MODEL)),
                ('employees_accounts', models.ManyToManyField(blank=True, related_name='employees_accounts', to=settings.AUTH_USER_MODEL, verbose_name='Employees')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='CustomerInfo_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Manager user of this client')),
            ],
        ),
        migrations.CreateModel(
            name='TranslationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_translate', models.TextField()),
                ('translated', models.TextField()),
                ('file_to_translate', models.FileField(null=True, upload_to='uploads_file_to_translate/%Y/%m/%d/')),
                ('star_ind', models.BooleanField(default=False, verbose_name='stared translation')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='last updated date')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='translation_client', to='translation.CustomerInfo')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='translation_history_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='translation_history_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
        ),
        migrations.CreateModel(
            name='TranslationDestinationPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation_way', models.CharField(choices=[('1', 'English/Arabic'), ('2', 'Arabic/English')], default='1', max_length=1, verbose_name='Translation from/to')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='main user')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_request', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='last updated date')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Subscription_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Subscription_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
        ),
        migrations.CreateModel(
            name='SiteLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Description')),
                ('number', models.IntegerField(blank=True, default=0, null=True, verbose_name='Label Number')),
                ('active_ind', models.BooleanField(default=True, verbose_name='Active')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='last updated date')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='site_label_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='site_label_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
        ),
        migrations.CreateModel(
            name='ManageFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_to_translate_ind', models.BooleanField(default=True, verbose_name='upload to translate text')),
                ('copy_translated_text_ind', models.BooleanField(default=True, verbose_name='copy translated text')),
                ('active_ind', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='last updated date')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='manage_features_created_by', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='translation.CustomerInfo')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='manage_features_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
        ),
        migrations.CreateModel(
            name='FileTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_en', models.FileField(blank=True, null=True, upload_to='translation_docs/')),
                ('status', models.CharField(blank=True, choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')], max_length=30, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='last updated date')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_translation_client', to='translation.CustomerInfo')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_translation_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_translation_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_used_requests', models.IntegerField(blank=True, default=0, null=True, verbose_name='Number of used requests')),
                ('active_ind', models.BooleanField(default=True, verbose_name='Active')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='last updated date')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_subscription_created_by', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='translation.CustomerInfo', verbose_name='Client')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='translation.Subscription')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_subscription_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
        ),
    ]
