from django import forms

from . import models


class AddObjectData(forms.Form):
    def __init__(self, object_name, *args, **kwargs):
        super().__init__()
        form_object = models.Object.objects.get(name=object_name)
        child_objects = models.Object.objects.filter(parent_object=form_object)
        fields = models.Field.objects.filter(object__in=child_objects)

        # Loop through all the fields
        field_list = {}
        for field in fields:
            data_type = field.data_type.name

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
                'DateTime': forms.DateTimeField()
            }

            self.fields[field.object.friendly_name] = form_fields[data_type]

            # Generate a list of fields including their order
            # If the order number isn't already in the list, add it
            if field_list.get(field.order) is None:
                field_list[field.order] = [field.object.friendly_name]
            else:
                # If the order number already has a field, add another field in the same position
                field_list[field.order] = [field_list[field.order][0], field.object.friendly_name]

        # Sort the field by order
        field_list = sorted(field_list.items())

        # Generate the list to order the fields by
        field_order = []
        for field in field_list:
            field_order.append(field[1][0])

        # Order the fields
        self.order_fields(field_order)
