# Generated by Django 2.0.7 on 2020-08-05 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '话题评论', 'verbose_name_plural': '话题评论'},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'verbose_name': '话题', 'verbose_name_plural': '话题'},
        ),
    ]
