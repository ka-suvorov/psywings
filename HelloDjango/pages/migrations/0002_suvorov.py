# Generated by Django 4.1.7 on 2023-03-02 19:03

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suvorov',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=220, verbose_name='Автор сайта')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField()),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
            ],
            options={
                'verbose_name': 'Об авторе',
                'ordering': ['title'],
            },
        ),
    ]
