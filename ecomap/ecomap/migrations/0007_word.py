# Generated by Django 5.0.1 on 2024-03-15 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomap', '0006_alter_user_last_played'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('word_id', models.AutoField(primary_key=True, serialize=False)),
                ('term', models.CharField(max_length=40)),
                ('definition', models.CharField(max_length=100)),
            ],
        ),
    ]
