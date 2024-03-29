# Generated by Django 4.0.6 on 2022-11-23 12:25

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(default='', unique=True, verbose_name='スラグ'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'このメールはすでに使われています.'}, help_text='この項目は必須です. 例:xxx@mail.com', max_length=254, unique=True, verbose_name='メール'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'このユーザー名はすでに使われています.'}, help_text='この項目は必須です. 150文字以下. 英数字, @/./+/-/_ だけが使えます.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='ユーザー名'),
        ),
    ]
