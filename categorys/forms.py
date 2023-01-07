from django import forms

from leads.models import Category


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
