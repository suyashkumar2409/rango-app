from django import forms
from rango.models import Category,Page

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128,help_text="Please enter category name")
	views = forms.IntegerField(widget = forms.HiddenInput(),initial=0)
	likes = forms.IntegerField(widget = forms.HiddenInput(),initial=0)
	slug = forms.CharField(widget = forms.HiddenInput(), required = False)

	class Meta:
		model = Category
		fields = ('name',)

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128,help_text="Please enter title of page")
	url = forms.URLField(max_length=200,help_text="Please enter url of page")
	views = forms.IntegerField(widget = forms.HiddenInput(),initial=0)

	class Meta:
		model = Page

		exclude = ('category',)

	def clean(self):

		cleandata = self.cleaned_data

		url = cleandata.get('url')

		if url and not url.startswith('http://'):
			url = 'http://'+url
			cleandata['url'] = url

		return cleandata