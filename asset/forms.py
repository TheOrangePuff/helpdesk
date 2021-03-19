from django import forms

from . import models


class AddObjectData(forms.Form):
    def __init__(self, object_name, *args, **kwargs):
        super().__init__()
        form_object = models.Object.objects.get(name=object_name)
        fields = models.Field.objects.filter(parent_object=form_object)

        # Loop through all the fields
        field_list = {}
        for field in fields:
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

            friendly_name = field.field_id.friendly_name
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
