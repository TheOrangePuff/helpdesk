import uuid

from django.db import models
import asset


# Object model
class Object(models.Model):
    name = models.SlugField(max_length=32, primary_key=True)
    friendly_name = models.CharField(max_length=32)
    desc = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


# Object data link model
class ObjectDataLink(models.Model):
    object_uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    object = models.ForeignKey("Object", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.object) + " - " + str(self.object_uid)

    def get_data(self):
        object_data = Data.objects.filter(object_uid=self)
        object_field_data = []

        for field_data in object_data:
            field_id = field_data.field_id
            field = Field.objects.get(name=field_id)
            data_type = field.data_type
            data_type_model = asset.models.__dict__.get(data_type.name)
            data = data_type_model.objects.get(data=field_data)

            if data_type_model == SingleChoice:
                object_uid = data.value.object_uid
                object_data = ObjectDataLink.objects.get(object_uid=object_uid).get_data()

                for object in object_data:
                    # TODO: get friendly field
                    friendly = object.data.field_id.friendly_field
                    object_field_data.append(object)
            else:
                object_field_data.append(data)

        return object_field_data


# Data type lookup table
class DataType(models.Model):
    name = models.CharField(max_length=32, primary_key=True)

    def __str__(self):
        return str(self.name)


# Data
class Data(models.Model):
    # Id of the object,
    # e.g. All the details about a person named Steve will have the uid of 1
    # Adding a new person will have the uid of 2
    object_uid = models.ForeignKey(ObjectDataLink, on_delete=models.CASCADE)
    field_id = models.ForeignKey("Field", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("object_uid", "field_id"), )

    def __str__(self):
        return "%s - %s" % (str(self.object_uid), str(self.field_id))

    # Get the data value
    # TODO: clean this function up
    def get_value(self):
        if hasattr(self, "shorttext"):
            return self.shorttext.value
        if hasattr(self, "longtext"):
            return self.longtext.value
        if hasattr(self, "boolean"):
            return self.boolean.value
        if hasattr(self, "image"):
            return self.image.value
        if hasattr(self, "file"):
            return self.file.value
        if hasattr(self, "integer"):
            return self.integer.value
        if hasattr(self, "positiveinteger"):
            return self.positiveinteger.value
        if hasattr(self, "date"):
            return self.date.value
        if hasattr(self, "time"):
            return self.time.value
        if hasattr(self, "datetime"):
            return self.datetime.value
        if hasattr(self, "singlechoice"):
            return self.singlechoice.value


# Types of data
# Short text
class ShortText(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.CharField(max_length=32)

    def __str__(self):
        return str(self.value)


# Long text
class LongText(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.CharField(max_length=1024)

    def __str__(self):
        return str(self.value)


# Boolean
class Boolean(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.BooleanField()

    def __str__(self):
        return str(self.value)


# Image
class Image(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.ImageField()


# File
class File(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.FileField()


# Integer
class Integer(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.IntegerField()

    def __str__(self):
        return str(self.value)


# Positive Integer
class PositiveInteger(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.PositiveIntegerField()

    def __str__(self):
        return str(self.value)


# Date
class Date(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.DateField()

    def __str__(self):
        return str(self.value)


# Time
class Time(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.TimeField()

    def __str__(self):
        return str(self.value)


# Date Time
class DateTime(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.DateTimeField()

    def __str__(self):
        return str(self.value)


# TODO: Multi-choice
class SingleChoice(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.ForeignKey(ObjectDataLink, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.value.get_data())


# Field
class Field(models.Model):
    name = models.SlugField(max_length=32, primary_key=True)
    friendly_name = models.CharField(max_length=32)
    desc = models.CharField(max_length=255)
    parent_object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='parent')
    data_type = models.ForeignKey(DataType, on_delete=models.PROTECT)
    friendly_field = models.BooleanField(default=False)
    order = models.fields.IntegerField(default=0)
    choice_type = models.ForeignKey(Object, on_delete=models.CASCADE, null=True, blank=True, related_name='choice_type')

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ["order"]
