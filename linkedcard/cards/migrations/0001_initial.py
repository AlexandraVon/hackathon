# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follow_id', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('template_id', models.AutoField(serialize=False, primary_key=True)),
                ('location', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=10)),
                ('headline', models.CharField(max_length=10)),
                ('photo_url', models.CharField(max_length=10)),
                ('linkedin_address', models.CharField(max_length=10)),
                ('company', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('qr_code_url', models.CharField(max_length=300)),
                ('temp_id', models.ForeignKey(to='cards.Template')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='relation',
            name='user_id',
            field=models.ForeignKey(to='cards.User'),
            preserve_default=True,
        ),
    ]
