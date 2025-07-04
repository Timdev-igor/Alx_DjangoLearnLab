# Generated by Django 5.1.6 on 2025-03-19 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('is_published', models.BooleanField(default=False)),
            ],
            options={
                'permissions': [('can_publish_post', 'Can publish post')],
            },
        ),
    ]
