# Generated by Django 3.1.2 on 2021-06-05 16:18

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketability', '0002_mfpclasses_mfpproducts_mfpproductshasmfpclasses_mfpshopsprices_mfpvardata_mntshopsprices_nbshopspric'),
    ]

    operations = [
        migrations.CreateModel(
            name='TxtHow',
            fields=[
                ('idtxt_how', models.AutoField(primary_key=True, serialize=False)),
                ('article_html_body', ckeditor_uploader.fields.RichTextUploadingField()),
                ('artice_title', models.TextField(blank=True, null=True)),
                ('article_description', models.TextField(blank=True, null=True)),
                ('article_keywords', models.TextField(blank=True, null=True)),
                ('cat', models.CharField(blank=True, max_length=3, null=True)),
                ('article_anno', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'txt_how',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TxtRatings',
            fields=[
                ('idtxt_ratings', models.AutoField(primary_key=True, serialize=False)),
                ('article_html_body', ckeditor_uploader.fields.RichTextUploadingField()),
                ('article_title', models.TextField(blank=True, null=True)),
                ('article_description', models.TextField(blank=True, null=True)),
                ('article_keywords', models.TextField(blank=True, null=True)),
                ('cat', models.CharField(blank=True, max_length=3, null=True)),
                ('article_anno', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'txt_ratings',
                'managed': False,
            },
        ),
    ]
