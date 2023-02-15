# Generated by Django 4.0 on 2023-02-15 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('decs', models.CharField(blank=True, max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('isbn', models.CharField(max_length=15, unique=True)),
                ('cover', models.TextField()),
                ('publish_date', models.DateField()),
                ('toc', models.TextField()),
                ('desc_detail', models.TextField()),
                ('page_count', models.IntegerField()),
                ('category_number', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='BookRank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('isbn', models.CharField(max_length=15, unique=True)),
                ('site', models.CharField(max_length=4)),
                ('period', models.CharField(max_length=4)),
                ('create_date', models.DateField()),
                ('rank_date', models.CharField(max_length=8)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book', to_field='isbn')),
            ],
        ),
    ]