# Generated by Django 5.0 on 2024-03-19 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0010_uploadfiles_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='women',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/%y/%m/%d', verbose_name='Фото'),
        ),
    ]
