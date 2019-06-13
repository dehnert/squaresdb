# Generated by Django 2.2 on 2019-06-09 03:25

from django.db import migrations, models
import django.db.models.deletion

def create_personfreqs(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    values = [
        dict(slug='every',      name='every',   order=10),
        dict(slug='monthly',    name='monthly', order=20),
        dict(slug='rarely',     name='rarely',  order=50),
        dict(slug='never',      name='never',   order=70),
        dict(slug='unknown',    name='unknown', order=90),
    ]

    model = apps.get_model('membership', 'PersonFrequency')
    model.objects.using(db_alias).bulk_create([
        model(**kwargs) for kwargs in values
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0007_user_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonFrequency',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('order', models.IntegerField(db_index=True)),
            ],
            options={
                'verbose_name_plural': 'person frequencies',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='frequency',
            field=models.ForeignKey(default='unknown', on_delete=django.db.models.deletion.PROTECT, to='membership.PersonFrequency', verbose_name='attendance frequency'),
            preserve_default=False,
        ),
        migrations.RunPython(create_personfreqs),
    ]