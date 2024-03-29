# Generated by Django 2.2 on 2019-06-10 04:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('membership', '0008_personfreq'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('in_gate', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPeriod',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPeriodPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('low', models.IntegerField()),
                ('high', models.IntegerField()),
                ('fee_cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='membership.FeeCategory')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gate.SubscriptionPeriod')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('at_dance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gate.Dance')),
                ('fee_cat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='membership.FeeCategory')),
                ('payment_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gate.PaymentMethod')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='membership.Person')),
            ],
        ),
        migrations.AddField(
            model_name='dance',
            name='period',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gate.SubscriptionPeriod'),
        ),
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gate.Dance')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gate.Payment')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='membership.Person')),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gate.Payment')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gate.SubscriptionPeriod')),
            ],
            bases=('gate.payment',),
        ),
        migrations.CreateModel(
            name='DancePayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gate.Payment')),
                ('for_dance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gate.Dance')),
            ],
            bases=('gate.payment',),
        ),
    ]
