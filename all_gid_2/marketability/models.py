# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class TxtHow(models.Model):
    idtxt_how = models.AutoField(primary_key=True)
    id_html_name = models.TextField(blank=True, null=True)
    article_html_body = RichTextUploadingField()
    article_title = models.TextField(blank=True, null=True)
    article_description = models.TextField(blank=True, null=True)
    article_keywords = RichTextUploadingField()
    cat = models.CharField(max_length=3, blank=True, null=True)
    article_anno = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    img = models.CharField(max_length=100, blank=True, null=True)
    pin = models.IntegerField()
    faq_question = models.CharField(max_length=255, blank=True, null=True)
    faq_unswer = RichTextUploadingField()

    class Meta:
        managed = False
        db_table = 'txt_how'


class TxtRatings(models.Model):
    idtxt_ratings = models.AutoField(primary_key=True)
    id_html_name = models.TextField(blank=True, null=True)
    article_html_body = RichTextUploadingField()
    article_title = models.TextField(blank=True, null=True)
    article_description = models.TextField(blank=True, null=True)
    article_keywords = RichTextUploadingField()
    cat = models.CharField(max_length=3, blank=True, null=True)
    article_anno = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    img = models.CharField(max_length=100, blank=True, null=True)
    pin = models.IntegerField()


    class Meta:
        managed = False
        db_table = 'txt_ratings'

    def __str__(self):
        return self.article_title

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MfpClasses(models.Model):
    type = models.CharField(max_length=2, blank=True, null=True)
    class_subtype = models.CharField(max_length=45, blank=True, null=True)
    text = models.CharField(max_length=100, blank=True, null=True)
    explanation = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mfp_classes'


class MfpProducts(models.Model):
    brand = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    prt_technology = models.CharField(max_length=45, blank=True, null=True)
    color = models.CharField(max_length=45, blank=True, null=True)
    format_a = models.CharField(max_length=45, blank=True, null=True)
    fax = models.CharField(max_length=3, blank=True, null=True)
    duplex = models.CharField(max_length=3, blank=True, null=True)
    photo = models.CharField(max_length=3, blank=True, null=True)
    usb = models.CharField(max_length=3, blank=True, null=True)
    wi_fi = models.CharField(max_length=3, blank=True, null=True)
    ethernet = models.CharField(max_length=3, blank=True, null=True)
    appear_month = models.DateField(blank=True, null=True)
    speed = models.CharField(max_length=45, blank=True, null=True)
    cis = models.CharField(max_length=3, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'mfp_products'


class MfpProductsHasMfpClasses(models.Model):
    fk_products = models.ForeignKey(MfpProducts, models.DO_NOTHING, db_column='fk_products')
    fk_classes = models.ForeignKey(MfpClasses, models.DO_NOTHING, db_column='fk_classes')

    class Meta:
        managed = False
        db_table = 'mfp_products_has_mfp_classes'


class MfpVardata(models.Model):
    month = models.DateField(blank=True, null=True)
    sales_units = models.IntegerField(blank=True, null=True)
    price_rur = models.FloatField(blank=True, null=True)
    fk_products = models.ForeignKey(MfpProducts, models.DO_NOTHING, db_column='fk_products', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mfp_vardata'


class MntClasses(models.Model):
    type = models.CharField(max_length=2, blank=True, null=True)
    class_subtype = models.CharField(max_length=45, blank=True, null=True)
    text = models.CharField(max_length=45, blank=True, null=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mnt_classes'


class MntProducts(models.Model):
    brand = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    resolution = models.CharField(max_length=45, blank=True, null=True)
    resolution_abb = models.CharField(max_length=45, blank=True, null=True)
    matrix_type = models.CharField(max_length=45, blank=True, null=True)
    curved = models.CharField(max_length=45, blank=True, null=True)
    game = models.CharField(max_length=45, blank=True, null=True)
    response_time = models.CharField(max_length=45, blank=True, null=True)
    appear_month = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mnt_products'


class MntProductsHasMntClasses(models.Model):
    fk_products = models.ForeignKey(MntProducts, models.DO_NOTHING, db_column='fk_products')
    fk_classes = models.ForeignKey(MntClasses, models.DO_NOTHING, db_column='fk_classes')

    class Meta:
        managed = False
        db_table = 'mnt_products_has_mnt_classes'
        unique_together = (('fk_products', 'fk_classes'),)


class MntVardata(models.Model):
    month = models.DateField(blank=True, null=True)
    sales_units = models.IntegerField(blank=True, null=True)
    price_rur = models.FloatField(blank=True, null=True)
    fk_products = models.ForeignKey(MntProducts, models.DO_NOTHING, db_column='fk_products', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mnt_vardata'


class NbClasses(models.Model):
    type = models.CharField(max_length=2, blank=True, null=True)
    class_subtype = models.CharField(max_length=45, blank=True, null=True)
    text = models.CharField(max_length=100, blank=True, null=True)
    explanation = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nb_classes'


class NbProducts(models.Model):
    brand = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    cluster = models.CharField(max_length=45, blank=True, null=True)
    target_market = models.CharField(max_length=10, blank=True, null=True)
    cpu_vendor = models.CharField(max_length=45, blank=True, null=True)
    base_platform = models.CharField(max_length=45, blank=True, null=True)
    gpu_list = models.CharField(max_length=45, blank=True, null=True)
    screen_size = models.CharField(max_length=45, blank=True, null=True)
    screen_resulution_list = models.CharField(max_length=45, blank=True, null=True)
    touchscreen = models.CharField(max_length=45, blank=True, null=True)
    appear_month = models.DateField(blank=True, null=True)
    classes_mtm = models.ManyToManyField(NbClasses, through='NbProductsHasNbClasses')

    class Meta:
        managed = False
        db_table = 'nb_products'


class NbProductsHasNbClasses(models.Model):
    fk_products = models.ForeignKey(NbProducts, models.DO_NOTHING, db_column='fk_products')
    fk_classes = models.ForeignKey(NbClasses, models.DO_NOTHING, db_column='fk_classes')

    class Meta:
        managed = False
        db_table = 'nb_products_has_nb_classes'
        unique_together = (('fk_products', 'fk_classes'),)


class NbVardata(models.Model):
    month = models.DateField(blank=True, null=True)
    sales_units = models.IntegerField(blank=True, null=True)
    price_rur = models.FloatField(blank=True, null=True)
    fk_products = models.ForeignKey(NbProducts, models.DO_NOTHING, db_column='fk_products', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nb_vardata'

class MfpShopsPrices(models.Model):
    fk_products_shop = models.ForeignKey(MfpProducts, models.DO_NOTHING, db_column='fk_products_shop')
    shop_name = models.CharField(max_length=20, blank=True, null=True)
    modification_name = models.CharField(max_length=255, blank=True, null=True)
    modfication_href = models.CharField(max_length=255, blank=True, null=True)
    modification_price = models.FloatField()
    month = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mfp_shops_prices'

class MntShopsPrices(models.Model):
    fk_products_shop = models.ForeignKey(MntProducts, models.DO_NOTHING, db_column='fk_products_shop')
    shop_name = models.CharField(max_length=20, blank=True, null=True)
    modification_name = models.CharField(max_length=255, blank=True, null=True)
    modfication_href = models.CharField(max_length=255, blank=True, null=True)
    modification_price = models.FloatField()
    month = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mnt_shops_prices'

class NbShopsPrices(models.Model):
    fk_products_shop = models.ForeignKey(NbProducts, models.DO_NOTHING, db_column='fk_products_shop')
    shop_name = models.CharField(max_length=20, blank=True, null=True)
    modification_name = models.CharField(max_length=255, blank=True, null=True)
    modfication_href = models.CharField(max_length=255, blank=True, null=True)
    modification_price = models.FloatField(blank=True, null=True)
    month = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nb_shops_prices'

class TextLinks(models.Model):
    category = models.CharField(max_length=3, blank=True, null=True)
    header = models.TextField(blank=True, null=True)
    annotation = models.TextField(blank=True, null=True)
    href = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'text_links'

class UpsClasses(models.Model):
    type = models.CharField(max_length=2, blank=True, null=True)
    class_subtype = models.CharField(max_length=45, blank=True, null=True)
    text = models.CharField(max_length=100, blank=True, null=True)
    explanation = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ups_classes'


class UpsProducts(models.Model):
    brand = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    appear_month = models.DateField(blank=True, null=True)
    power = models.CharField(max_length=45, blank=True, null=True)
    type_line = models.CharField(max_length=45, blank=True, null=True)
    form_factor = models.CharField(max_length=45, blank=True, null=True)
    level = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ups_products'


class UpsProductsHasUpsClasses(models.Model):
    fk_products = models.ForeignKey(UpsProducts, models.DO_NOTHING, db_column='fk_products', blank=True, null=True)
    fk_classes = models.ForeignKey(UpsClasses, models.DO_NOTHING, db_column='fk_classes', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ups_products_has_ups_classes'


class UpsShopsPrices(models.Model):
    fk_products_shop = models.ForeignKey(UpsProducts, models.DO_NOTHING, db_column='fk_products_shop')
    shop_name = models.CharField(max_length=20, blank=True, null=True)
    month = models.CharField(max_length=255, blank=True, null=True)
    modfication_href = models.CharField(max_length=255, blank=True, null=True)
    modification_price = models.FloatField()
    modification_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ups_shops_prices'

class UpsVardata(models.Model):
    id = models.IntegerField(primary_key=True)
    month = models.DateField(blank=True, null=True)
    sales_units = models.IntegerField(blank=True, null=True)
    price_rur = models.FloatField(blank=True, null=True)
    fk_products = models.ForeignKey(UpsProducts, models.DO_NOTHING, db_column='fk_products')

    class Meta:
        managed = False
        db_table = 'ups_vardata'