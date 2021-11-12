category = forms.ChoiceField(choices=[(cat.id, cat.name) for cat in Category.objects.all()],
                             widget = forms.Select(attrs={'class': 'form-control'}))