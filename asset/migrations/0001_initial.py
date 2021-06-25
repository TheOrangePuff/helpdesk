# Generated by Django 3.1.7 on 2021-06-09 01:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DataType',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('friendly_name', models.CharField(max_length=32)),
                ('desc', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Boolean',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='asset.data')),
                ('value', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='asset.data')),
                ('value', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DateTime',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='asset.data')),
                ('value', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='asset.data')),
                ('value', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='asset.data')),
                ('value', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Integer',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='asset.data')),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LongText',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='asset.data')),
                ('value', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='PositiveInteger',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='asset.data')),
                ('value', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ShortText',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='asset.data')),
                ('value', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='asset.data')),
                ('value', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ObjectDataLink',
            fields=[
                ('object_uid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.object')),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('friendly_name', models.CharField(max_length=32)),
                ('desc', models.CharField(max_length=255)),
                ('friendly_field', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('choice_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='choice_type', to='asset.object')),
                ('data_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='asset.datatype')),
                ('parent_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='asset.object')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='data',
            name='field_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.field'),
        ),
        migrations.AddField(
            model_name='data',
            name='object_uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.objectdatalink'),
        ),
        migrations.CreateModel(
            name='SingleChoice',
            fields=[
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='asset.data')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.objectdatalink')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='data',
            unique_together={('object_uid', 'field_id')},
        ),
    ]