# Generated by Django 2.1.7 on 2019-04-26 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.CharField(max_length=255, unique=True, verbose_name='Slug')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is published')),
                ('keywords', models.CharField(blank=True, help_text='Separate by comma and space', max_length=255, null=True, verbose_name='Keywords')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site', verbose_name='Site')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together={('slug', 'site')},
        ),
    ]
