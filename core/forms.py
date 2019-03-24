from django import forms


class BasicSearchForm(forms.Form):
    """
    Search is passed directly into the
    NASA image search API's free text
    search parameter, q.
    """
    q = forms.CharField(label='', max_length=200, required=False)


class AdvancedSearchForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200, required=False)
    # center = forms.CharField(label='Center', max_length=100, required=False)
    # description = forms.CharField(
    #    label='Description', max_length=200, required=False)
    keywords = forms.CharField(
        label='Keywords (comma separated)', max_length=200, required=False)
    location = forms.CharField(
        label='Location', max_length=100, required=False)
    photographer = forms.CharField(
        label='Photographer', max_length=100, required=False)
    year_start = forms.DateField(
        label='Year start', input_formats=['%Y'], required=False)
    year_end = forms.DateField(label='Year end', input_formats=[
                               '%Y'], required=False)
    nasa_id = forms.CharField(label='NASA ID', max_length=50, required=False)
