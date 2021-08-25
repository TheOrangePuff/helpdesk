from django import forms

from . import models


class AddObjectData(forms.Form):
    def __init__(self, *args, **kwargs):
        self.object_name = kwargs.pop("object_name")
        super(AddObjectData, self).__init__(*args, **kwargs)
        self.form_object = models.Object.objects.get(name=self.object_name)
        self.dynamic_fields = models.Field.objects.filter(parent_object=self.form_object)

        # Loop through all the fields
        field_list = {}
        for field in self.dynamic_fields:
            choices = []
            data_type = field.data_type.name

            if field.choice_type:
                choice_type = field.choice_type.name
                data_objects_list = models.ObjectDataLink.objects.filter(object=choice_type)
                # Loop through all objects of that specific type
                for data in data_objects_list:
                    friendly_name_list = []
                    # Prioritise friendly field, then fallback to order
                    # Get a list of all the friendly fields
                    friendly_name_fields = models.Field.objects.filter(parent_object=choice_type, friendly_field=True)
                    if friendly_name_fields:
                        for friendly_field in friendly_name_fields:
                            friendly_field_data = models.Data.objects.get(field_id=friendly_field, object_uid=data)
                            friendly_name_list.append(friendly_field_data.get_value())
                    else:
                        # If no friendly field has been set, get the first field of the object
                        friendly_name_field = models.Field.objects.filter(parent_object=choice_type).first()
                        friendly_field_data = models.Data.objects.get(field_id=friendly_name_field, object_uid=data)
                        friendly_name_list.append(friendly_field_data.get_value())

                    # Join all the fields names together with a space inbetween
                    friendly_name = " ".join(friendly_name_list)

                    # Append the data to the choice field
                    choices.append((data.object_uid, friendly_name))

            # Change the field type depending on the data type
            form_fields = {
                'ShortText': forms.CharField(max_length=32),
                'LongText': forms.CharField(max_length=1024),
                'Boolean': forms.BooleanField(),
                'Image': forms.ImageField(),
                'File': forms.FileField(),
                'Integer': forms.IntegerField(),
                'PositiveInteger': forms.IntegerField(),
                'Date': forms.DateField(),
                'Time': forms.TimeField(),
                'DateTime': forms.DateTimeField(),
                'SingleChoice': forms.ChoiceField(choices=choices)
            }

            friendly_name = field.friendly_name
            self.fields[friendly_name] = form_fields[data_type]

            # Generate a list of fields including their order
            # If the order number isn't already in the list, add it
            if field_list.get(field.order) is None:
                field_list[field.order] = [friendly_name]
            else:
                # If the order number already has a field, add another field in the same position
                field_list[field.order] = [field_list[field.order][0], friendly_name]

        # Sort the field by order
        field_list = sorted(field_list.items())

        # Generate the list to order the fields by
        field_order = []
        for field in field_list:
            field_order.append(field[1][0])

        # Order the fields
        self.order_fields(field_order)

    def save(self, commit=False):
        # Create the object data link
        object_data_link = models.ObjectDataLink.objects.create(object=self.form_object)

        for field in self.dynamic_fields:
            # Get the data type
            data_type = field.data_type
            data_type_model = models.__dict__.get(data_type.name)
            # Create a link to the data
            data = models.Data.objects.create(object_uid=object_data_link, field_id=field)
            # Create the record in the appropriate data type table
            value = self.data[field.friendly_name]
            if field.data_type_id == 'SingleChoice':
                value = models.ObjectDataLink.objects.get(object_uid=self.data[field.friendly_name])

            record = data_type_model.objects.create(data=data, value=value)

    def is_valid(self):
        return True


class ObjectCreationForm(forms.ModelForm):
    class Meta:
        model = models.Object
        fields = ['name', 'friendly_name', 'desc']


class FieldCreationForm(forms.ModelForm):
    class Meta:
        model = models.Field
        fields = ['name', 'friendly_name', 'desc', 'data_type', 'friendly_field', 'order', 'parent_object']
        widgets = {
            'order': forms.HiddenInput(),
            'parent_object': forms.HiddenInput()
        }

    def __init__(self, *args, parent_object, **kwargs):
        self.parent_object = models.Object.objects.get(name=parent_object)

        super().__init__(*args, **kwargs)
        self.fields.get('order').required = False
        self.fields.get('parent_object').required = False

    # If the field doesn't have a parent object, assign it a parent object
    def clean_parent_object(self):
        data = self.cleaned_data['parent_object']
        if not data:
            self.cleaned_data['parent_object'] = self.parent_object
            data = self.cleaned_data['parent_object']

        return data
