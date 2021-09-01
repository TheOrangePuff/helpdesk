# Generated by Django 3.1.3 on 2021-08-27 01:05

import asset.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_auto_20210609_0200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='field',
            options={'ordering': ['parent_object', 'order']},
        ),
        migrations.AlterField(
            model_name='field',
            name='choice_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='choice_type', to='asset.object'),
        ),
        migrations.AlterField(
            model_name='field',
            name='data_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='asset.datatype'),
        ),
        migrations.AlterField(
            model_name='field',
            name='order',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='field',
            unique_together={('parent_object', 'order')},
        ),
    ]