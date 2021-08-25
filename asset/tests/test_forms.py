from django.test import TestCase
from asset.forms import FieldCreationForm
from asset.models import Object, Field, DataType


class FieldCreationFormTestCase(TestCase):
    fixtures = ['datatypes.json']

    @classmethod
    def setUpTestData(cls):
        # Create an object to test with and populate it with some fields
        obj = Object.objects.create(name='laptop', friendly_name='Laptop', desc='A laptop',
                                    active=True)
        Field.objects.create(name='laptop_serial', friendly_name='Serial Number',
                             desc='Serial number of the laptop',
                             data_type=DataType.objects.get(name='ShortText'),
                             order=0, parent_object=obj)
        Field.objects.create(name='laptop_name', friendly_name='Name',
                             desc='Name of the laptop',
                             data_type=DataType.objects.get(name='ShortText'),
                             friendly_field=True, order=1, parent_object=obj)
        Field.objects.create(name='laptop_brand', friendly_name='Brand',
                             desc='Brand of the laptop',
                             data_type=DataType.objects.get(name='ShortText'),
                             order=2, parent_object=obj)

    def test_form_submit(self):
        form_data = {'name': 'operating_system', 'friendly_name': 'OS',
                     'desc': 'The operating system the laptop is running.',
                     'data_type': 'ShortText'}

        form = FieldCreationForm(parent_object='laptop', data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_form_invalid(self):
        form_data = {'name': 'Operating System', 'friendly_name': 'OS',
                     'desc': 'The operating system the laptop is running.',
                     'data_type': 'ShortText'}

        form = FieldCreationForm(parent_object='laptop', data=form_data)

        self.assertFalse(form.is_valid())
