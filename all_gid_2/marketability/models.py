from django.db import models

# Create your models here.
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


class MntClasses(models.Model):
    type = models.CharField(max_length=2, blank=True, null=True)
    class_subtype = models.CharField(max_length=45, blank=True, null=True)
    text = models.CharField(max_length=45, blank=True, null=True)
    explanation = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mnt_classes'


class MntProducts(models.Model):
    brand = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    screen_size = models.CharField(max_length=45, blank=True, null=True)

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
