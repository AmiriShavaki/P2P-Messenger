# Generated by Django 4.2.2 on 2023-06-09 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_by_me', models.BooleanField(default=False)),
                ('text', models.CharField(max_length=1200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
    ]
