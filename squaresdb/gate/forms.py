import datetime

from django import forms

import squaresdb.gate.models as gate_models
import squaresdb.membership.models as member_models

class NewPeriodForm(forms.ModelForm):
    # TODO: Add SubscriptionPeriodPrice for every fee cat
    # TODO: Need to create dance objects
    # TODO: Choose default price scheme
    # Form is:
    # - Basic period info (name, slug, dates)
    # - default price scheme just one)
    # - prices for every fee cat
    # Then we create dance objects
    # So I think this is a overall form + SubscriptionPeriodPrice formset
    # https://docs.djangoproject.com/en/4.0/topics/forms/formsets/#using-more-than-one-formset-in-a-view
    seasons = ['fall', 'winter', 'spring', 'summer']
    season = forms.ChoiceField(choices=zip(seasons, seasons))
    price_qset = gate_models.DancePriceScheme.objects.all().order_by('-active', 'name')
    default_price_scheme = forms.ModelChoiceField(queryset=price_qset, empty_label=None)

    def default_year(self):
        if self.is_valid():
            # As a side effect, populates cleaned_data
            pass
        print(f'{self.cleaned_data=}')
        start = self.cleaned_data.get('start_date')
        end = self.cleaned_data.get('end_date')
        if start and end:
            mid = start + ((end-start)/2)
            return mid.year
        return None

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        print(f'{self.fields=}')
        print(f'{self.fields["name"].__dict__=}')
        if data:
            #year = self.default_year() or "year"
            year = (datetime.date.today() + datetime.timedelta(days=90)).year
            season = data.get('season', 'season')
            #self.fields['name'].initial = '%s %s' % (season.capitalize(), year)
            self.initial['name'] = '%s %s' % (season.capitalize(), year)
            self.fields['slug'].initial = '%s-%s' % (year, season.capitalize())
        else:
            del self.fields['name']
            #self.fields['name'].widget = forms.HiddenInput()
            self.fields['slug'].widget = forms.HiddenInput()

    class Meta:
        model = gate_models.SubscriptionPeriod
        fields = ['start_date', 'end_date', 'season', 'name', 'slug',
                  'default_price_scheme']

class NewPeriodPriceForm(forms.ModelForm):
    class Meta:
        model = gate_models.SubscriptionPeriodPrice
        fields = ('fee_cat', 'low', 'high')

def new_period_prices_formset(submit=None):
    fee_cats = list(member_models.FeeCategory.objects.all())
    SubPriceFormset = forms.inlineformset_factory(gate_models.SubscriptionPeriod,
            gate_models.SubscriptionPeriodPrice,
            form=NewPeriodPriceForm, extra=len(fee_cats))
    initial = [{'fee_cat': fee_cat} for fee_cat in fee_cats]
    formset = SubPriceFormset(initial=initial)
    for form in formset:
        form.fields['fee_cat'].disabled = True
    return formset
