from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from accounts.models import Charity, Benefactor, User, ContactInfo


class CharitySignUpForm(UserCreationForm):

    charity_name = forms.CharField(required=True)
    """

    provinces = ('Tehran','Qom' , 'Yazd' , 'Shiraz')
    province = forms.MultipleChoiceField(
        required=True,
        widget=forms.ChoiceField,
        choices=provinces,
    )

    city = forms.CharField(max_length=30)
    postal_code = forms.CharField(max_length=30)
    address = forms.CharField(max_length=500)
    phone_number = forms.CharField(max_length=20)

    """
   # grade = forms.CharField(max_length=20)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_charity = True
        user.save()
       # charity = Charity.objects.create(user=user)
       # contact_info = ContactInfo.objects.create(user=user)

        """
        
        charity.charity_name = self.cleaned_data.get('charity_name')

        
        contact_info.country = 'Iran'
        contact_info.province = self.cleaned_data.get('province')
        contact_info.city = self.cleaned_data.get('city')
        contact_info.postal_code = self.cleaned_data.get('postal_code')
        contact_info.address = self.cleaned_data.get('address')
        contact_info.phone_number=self.cleaned_data.get('phone_number')

        """

       # contact_info.save()
       # charity.save()
        return user
