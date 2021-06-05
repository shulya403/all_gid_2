# Generated by Django 3.1.2 on 2021-05-29 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketability', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MfpClasses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=2, null=True)),
                ('class_subtype', models.CharField(blank=True, max_length=45, null=True)),
                ('text', models.CharField(blank=True, max_length=100, null=True)),
                ('explanation', models.CharField(blank=True, max_length=256, null=True)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'mfp_classes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MfpProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(blank=True, max_length=45, null=True)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('type', models.CharField(blank=True, max_length=45, null=True)),
                ('prt_technology', models.CharField(blank=True, max_length=45, null=True)),
                ('color', models.CharField(blank=True, max_length=45, null=True)),
                ('format_a', models.CharField(blank=True, max_length=45, null=True)),
                ('fax', models.CharField(blank=True, max_length=3, null=True)),
                ('duplex', models.CharField(blank=True, max_length=3, null=True)),
                ('photo', models.CharField(blank=True, max_length=3, null=True)),
                ('usb', models.CharField(blank=True, max_length=3, null=True)),
                ('wi_fi', models.CharField(blank=True, max_length=3, null=True)),
                ('ethernet', models.CharField(blank=True, max_length=3, null=True)),
                ('appear_month', models.DateField(blank=True, null=True)),
                ('speed', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'mfp_products',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MfpProductsHasMfpClasses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'mfp_products_has_mfp_classes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MfpShopsPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(blank=True, max_length=20, null=True)),
                ('modification_name', models.CharField(blank=True, max_length=255, null=True)),
                ('modfication_href', models.CharField(blank=True, max_length=255, null=True)),
                ('modification_price', models.FloatField()),
                ('month', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'mfp_shops_prices',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MfpVardata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(blank=True, null=True)),
                ('sales_units', models.IntegerField(blank=True, null=True)),
                ('price_rur', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'mfp_vardata',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MntShopsPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(blank=True, max_length=20, null=True)),
                ('modification_name', models.CharField(blank=True, max_length=255, null=True)),
                ('modfication_href', models.CharField(blank=True, max_length=255, null=True)),
                ('modification_price', models.FloatField()),
                ('month', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'mnt_shops_prices',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NbShopsPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(blank=True, max_length=20, null=True)),
                ('modification_name', models.CharField(blank=True, max_length=255, null=True)),
                ('modfication_href', models.CharField(blank=True, max_length=255, null=True)),
                ('modification_price', models.FloatField(blank=True, null=True)),
                ('month', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'nb_shops_prices',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TextLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=3, null=True)),
                ('header', models.TextField(blank=True, null=True)),
                ('annotation', models.TextField(blank=True, null=True)),
                ('href', models.TextField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'text_links',
                'managed': False,
            },
        ),
    ]
