# Generated by Django 2.2.7 on 2020-03-21 04:31

from django.db import migrations, models
import django.db.models.deletion


def add_initial_price_scheme(apps, schema_editor):
    PriceScheme = apps.get_model('gate', 'DancePriceScheme')
    scheme = PriceScheme(name='normal')
    scheme.save()


def migrate_foreign_to_many(apps, schema_editor):
    """Copy the value of the period field to the periods field"""
    SubPay = apps.get_model('gate', 'SubscriptionPayment')
    for payment in SubPay.objects.all():
        payment.periods.add(payment.period)


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0008_personfreq'),
        ('gate', '0003_add_signin_app_perm'),
    ]

    operations = [
        migrations.CreateModel(
            name='DancePriceScheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.RunPython(add_initial_price_scheme),
        migrations.AddField(
            model_name='dance',
            name='price_scheme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gate.DancePriceScheme', default=1),
            preserve_default=False),
        migrations.AddField(
            model_name='subscriptionpayment',
            name='periods',
            field=models.ManyToManyField(to='gate.SubscriptionPeriod'),
        ),
        migrations.RunPython(migrate_foreign_to_many),
        migrations.RemoveField(
            model_name='subscriptionpayment',
            name='period',
        ),
        migrations.CreateModel(
            name='DancePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('low', models.IntegerField()),
                ('high', models.IntegerField()),
                ('fee_cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='membership.FeeCategory')),
                ('price_scheme', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gate.DancePriceScheme')),
            ],
        ),
    ]