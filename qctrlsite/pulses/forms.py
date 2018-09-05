from django import forms


class PulseForm(forms.Form):
    """
    Handles the creation of a new pulse with all information.
    """
    name = forms.CharField(label='Pulse name', max_length=50)
    ptype = forms.CharField(label='Pulse type', max_length=9)

    rabi = forms.FloatField(required=False, min_value=0, max_value=100,
                            widget=forms.NumberInput(
                                attrs={'id' : 'form_rabi',
                                       'step' : "0.01"}))

    angle = forms.FloatField(required=False, min_value=0, max_value=1,
                             widget=forms.NumberInput(
                                 attrs={'id' : 'form_angle',
                                        'step' : "0.0001"}))


class PulseNameForm(forms.Form):
    """
    Handles gettings a single pulse name.
    """
    name = forms.CharField(label='Pulse name', max_length=50)


class UploadForm(forms.Form):
    """
    Handles the upload of a single file.
    """
    filea = forms.FileField()


class UpdateForm(forms.Form):
    """
    Handles the update of a pulse and can take initial values
    of existing pulse as input values.
    """
    name = forms.CharField(label='Pulse name', max_length=50, initial='')
    ptype = forms.CharField(label='Pulse type', max_length=9)

    rabi = forms.FloatField(required=False, min_value=0, max_value=100,
                            widget=forms.NumberInput(
                                attrs={'id' : 'form_rabi',
                                       'step' : "0.01"}))

    angle = forms.FloatField(required=False, min_value=0, max_value=1,
                             widget=forms.NumberInput(
                                 attrs={'id' : 'form_angle',
                                        'step' : "0.0001"}))


    def __init__(self, *args, **kwargs):

        if('initial_name' in kwargs):
            initial_name = kwargs['initial_name']
            del kwargs['initial_name']
        else:
            initial_name = ''

        if('initial_ptype' in kwargs):
            initial_ptype = kwargs['initial_ptype']
            del kwargs['initial_ptype']
        else:
            initial_ptype = ''

        if('initial_rabi' in kwargs):
            initial_rabi = kwargs['initial_rabi']
            del kwargs['initial_rabi']
        else:
            initial_rabi = 0.0

        if('initial_angle' in kwargs):
            initial_angle = kwargs['initial_angle']
            del kwargs['initial_angle']
        else:
            initial_angle = 0.0

        super().__init__(*args, **kwargs)

        self.fields['name'].initial = initial_name
        self.fields['ptype'].initial = initial_ptype
        self.fields['rabi'].initial = initial_rabi
        self.fields['angle'].initial = initial_angle
