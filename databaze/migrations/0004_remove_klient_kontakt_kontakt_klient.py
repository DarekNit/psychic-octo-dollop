# Generated by Django 4.0.5 on 2022-06-23 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('databaze', '0003_remove_pojisteni_id_smlouvy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='klient',
            name='kontakt',
        ),
        migrations.AddField(
            model_name='kontakt',
            name='klient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='databaze.klient'),
        ),
    ]
