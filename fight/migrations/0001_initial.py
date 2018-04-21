# Generated by Django 2.0.4 on 2018-04-21 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comeback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comeback_text', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health', models.IntegerField()),
                ('current_fight', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fight.Fight')),
            ],
        ),
        migrations.CreateModel(
            name='Insult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insult_text', models.CharField(max_length=1000)),
                ('correct_comeback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fight.Comeback')),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('fight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fight.Fight')),
                ('insult', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fight.Insult')),
            ],
        ),
    ]
