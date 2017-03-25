from django import forms

class ItemForm(forms.Form):
    quantity= forms.IntegerField(label="Input the quantity",initial=1,max_value=50,min_value=1)
    search= forms.CharField(max_length=250,widget=forms.TextInput(attrs={'placeholder': 'Enter state/city/pincode'}))

class SearchForm(forms.Form):
    search= forms.CharField(label="Search in another area",max_length=250,widget=forms.TextInput(attrs={'placeholder': 'Enter state/city/pincode'}))
    quantity= forms.IntegerField(initial=1,max_value=50,min_value=1)
