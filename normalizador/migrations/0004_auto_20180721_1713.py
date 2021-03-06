# Generated by Django 2.0.7 on 2018-07-21 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('normalizador', '0003_auto_20180721_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barrio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=127)),
                ('estado', models.IntegerField(choices=[(1, 'Activo'), (2, 'Inactivo')], db_index=True, default=1)),
                ('cuadrante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='normalizador.Cuadrante')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='barrio',
            unique_together={('nombre', 'cuadrante')},
        ),
    ]
