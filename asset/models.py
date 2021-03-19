import uuid

from django.db import models


# Object model
class Object(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    friendly_name = models.CharField(max_length=32)
    desc = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Object data link model
class ObjectDataLink(models.Model):
    object_uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    object = models.ForeignKey("Object", on_delete=models.CASCADE)

    def __str__(self):
        return self.object_uid.__str__()


# Data type lookup table
class DataType(models.Model):
    name = models.CharField(max_length=32, primary_key=True)

    def __str__(self):
        return self.name


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
        return "%s - %s" % (self.object_uid.__str__(), self.field_id.__str__())

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
        return self.value


# Long text
class LongText(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.CharField(max_length=1024)

    def __str__(self):
        return self.value


# Boolean
class Boolean(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.BooleanField()

    def __str__(self):
        return self.value


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
        return self.value


# Positive Integer
class PositiveInteger(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.PositiveIntegerField()

    def __str__(self):
        return self.value


# Date
class Date(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.DateField()

    def __str__(self):
        return self.value


# Time
class Time(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.TimeField()

    def __str__(self):
        return self.value


# Date Time
class DateTime(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.DateTimeField()

    def __str__(self):
        return self.value


# TODO: Multi-choice
class SingleChoice(models.Model):
    data = models.OneToOneField(Data, on_delete=models.PROTECT, primary_key=True)
    value = models.ForeignKey(ObjectDataLink, on_delete=models.CASCADE)

    def __str__(self):
        return self.value


# Field
class Field(models.Model):
    field_id = models.OneToOneField(Object, on_delete=models.PROTECT, primary_key=True)
    parent_object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='parent')
    data_type = models.ForeignKey(DataType, on_delete=models.PROTECT)
    friendly_field = models.BooleanField(default=False)
    order = models.fields.IntegerField(default=0)
    choice_type = models.ForeignKey(Object, on_delete=models.CASCADE, null=True, blank=True, related_name='choice_type')

    def __str__(self):
        return self.field_id.__str__()

    class Meta:
        ordering = ["order"]
