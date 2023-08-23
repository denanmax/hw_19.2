from django import forms

from catalog.models import Product, Category, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProhibitedWordsMixin:
    def clean(self):
        cleaned_data = super().clean()
        name = self.cleaned_data['name'].lower()
        description = self.cleaned_data['description'].lower()

        prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in prohibited_words:
            if word in name.lower():
                raise forms.ValidationError('Плохое название')
            if word in description.lower():
                raise forms.ValidationError('Плохое описание')

        return cleaned_data


class ProductForm(StyleFormMixin, ProhibitedWordsMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    # def clean_name(self):
    #     cleaned_data = self.cleaned_data['name'].lower()
    #     prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
    #                        'радар']
    #
    #     for word in prohibited_words:
    #         if word in cleaned_data:
    #             raise forms.ValidationError('Плохое слово')
    #
    #     return cleaned_data.lower()



class Category_form(StyleFormMixin, ProhibitedWordsMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
