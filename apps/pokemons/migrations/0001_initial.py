# Generated by Django 3.1.2 on 2020-10-12 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NameStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Specie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('capture_rate', models.IntegerField()),
                ('color', models.CharField(max_length=80)),
                ('flavor_text', models.TextField()),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('abilities', models.ManyToManyField(to='pokemons.Ability')),
                ('moves', models.ManyToManyField(to='pokemons.Move')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemons.namestatistic')),
                ('specie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='pokemons.specie')),
            ],
        ),
        migrations.CreateModel(
            name='Sprite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('back_default', models.URLField(blank=True, null=True)),
                ('back_female', models.URLField(blank=True, null=True)),
                ('back_shiny', models.URLField(blank=True, null=True)),
                ('back_shiny_female', models.URLField(blank=True, null=True)),
                ('front_default', models.URLField(blank=True, null=True)),
                ('front_female', models.URLField(blank=True, null=True)),
                ('front_shiny', models.URLField(blank=True, null=True)),
                ('front_shiny_female', models.URLField(blank=True, null=True)),
                ('specie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sprites', to='pokemons.specie')),
            ],
        ),
        migrations.AddField(
            model_name='specie',
            name='types',
            field=models.ManyToManyField(to='pokemons.Type'),
        ),
        migrations.CreateModel(
            name='Captured',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick_name', models.CharField(max_length=80)),
                ('is_party_member', models.BooleanField()),
                ('specie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemons.specie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
