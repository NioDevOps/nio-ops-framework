# Generated by Django 2.1.7 on 2019-04-29 06:01

import concurrency.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_cryptography.fields
import django_extensions.db.fields.json
import mptt.fields
import polymorphic_tree.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=32, verbose_name='中文名')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaseResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_version', concurrency.fields.IntegerVersionField(default=0, help_text='record revision number')),
                ('_ctime', models.DateTimeField(auto_now_add=True)),
                ('_mtime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, verbose_name='资源名')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='BaseService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_version', concurrency.fields.IntegerVersionField(default=0, help_text='record revision number')),
                ('_ctime', models.DateTimeField(auto_now_add=True)),
                ('_mtime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('tree_path_cache', models.CharField(blank=True, max_length=255, null=True)),
                ('info', models.CharField(max_length=255)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'verbose_name': 'Tree node',
                'verbose_name_plural': 'Tree nodes',
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='中文名')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('leaders', models.ManyToManyField(default=[], related_name='leader_ships', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='rest.Department')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'ipv4'), (2, 'ipv6'), (3, 'host'), (4, 'url')])),
                ('address', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('k', models.CharField(max_length=64, verbose_name='k')),
                ('v', models.CharField(max_length=64, verbose_name='v')),
            ],
        ),
        migrations.CreateModel(
            name='ServerType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_version', concurrency.fields.IntegerVersionField(default=0, help_text='record revision number')),
                ('_ctime', models.DateTimeField(auto_now_add=True)),
                ('_mtime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, verbose_name='机器类型')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceResourcesRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_ctime', models.DateTimeField(auto_now_add=True)),
                ('_mtime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_version', concurrency.fields.IntegerVersionField(default=0, help_text='record revision number')),
                ('_ctime', models.DateTimeField(auto_now_add=True)),
                ('_mtime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('baseresource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rest.BaseResource')),
                ('cpu', models.IntegerField()),
                ('mem', models.IntegerField()),
                ('replicas', models.IntegerField(default=3)),
                ('extra_args', django_extensions.db.fields.json.JSONField(default={})),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('rest.baseresource',),
        ),
        migrations.CreateModel(
            name='Db',
            fields=[
                ('baseresource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rest.BaseResource')),
                ('user', models.CharField(max_length=64, verbose_name='管理账户')),
                ('password', django_cryptography.fields.encrypt(models.CharField(max_length=50))),
                ('extra_args', django_extensions.db.fields.json.JSONField(default={})),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('rest.baseresource',),
        ),
        migrations.CreateModel(
            name='DbInstance',
            fields=[
                ('baseresource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rest.BaseResource')),
                ('manage_user', models.CharField(max_length=64, verbose_name='管理账户')),
                ('manage_password', django_cryptography.fields.encrypt(models.CharField(max_length=50))),
                ('port', models.IntegerField(default=3306)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('rest.baseresource',),
        ),
        migrations.CreateModel(
            name='DbService',
            fields=[
                ('baseservice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rest.BaseService')),
                ('use_type', models.CharField(choices=[('shard', 'shard'), ('main-subordinate', 'main-subordinate'), ('pxc', 'pxc')], max_length=255)),
            ],
            options={
                'verbose_name': 'db-service',
                'verbose_name_plural': 'db-services',
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('rest.baseservice',),
        ),
        migrations.CreateModel(
            name='K8sCluster',
            fields=[
                ('baseresource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rest.BaseResource')),
                ('admin_token', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('rest.baseresource',),
        ),
        migrations.CreateModel(
            name='NormalService',
            fields=[
                ('baseservice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rest.BaseService')),
                ('git', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'normal-service',
                'verbose_name_plural': 'normal-services',
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('rest.baseservice',),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('baseresource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rest.BaseResource')),
                ('server_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rest.ServerType')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('rest.baseresource',),
        ),
        migrations.AddField(
            model_name='version',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rest.BaseService'),
        ),
        migrations.AddField(
            model_name='serviceresourcesrelation',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.BaseResource'),
        ),
        migrations.AddField(
            model_name='serviceresourcesrelation',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.BaseService'),
        ),
        migrations.AddField(
            model_name='serviceresourcesrelation',
            name='version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='rest.Version'),
        ),
        migrations.AddField(
            model_name='label',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='rest.BaseResource'),
        ),
        migrations.AddField(
            model_name='interface',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='rest.BaseResource'),
        ),
        migrations.AddField(
            model_name='baseservice',
            name='parent',
            field=polymorphic_tree.models.PolymorphicTreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='rest.BaseService'),
        ),
        migrations.AddField(
            model_name='baseservice',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_rest.baseservice_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='baseservice',
            name='resources',
            field=models.ManyToManyField(blank=True, through='rest.ServiceResourcesRelation', to='rest.BaseResource'),
        ),
        migrations.AddField(
            model_name='baseresource',
            name='departments',
            field=models.ManyToManyField(default=[], to='rest.Department'),
        ),
        migrations.AddField(
            model_name='baseresource',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_rest.baseresource_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='user',
            name='departments',
            field=models.ManyToManyField(related_name='members', to='rest.Department'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='label',
            unique_together={('resource', 'k', 'v')},
        ),
        migrations.AlterIndexTogether(
            name='label',
            index_together={('resource', 'k', 'v')},
        ),
        migrations.AddField(
            model_name='dbinstance',
            name='base_resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='belong_resource', to='rest.BaseResource'),
        ),
        migrations.AddField(
            model_name='db',
            name='db_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.DbInstance'),
        ),
        migrations.AddField(
            model_name='container',
            name='k8s_cluster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rest.K8sCluster'),
        ),
    ]
