import uuid

from django.db import models


# Object model
class Object(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    friendly_name = models.CharField(max_length=32, default=name.__str__())
    desc = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    parent_object = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


# Object data link model
class ObjectDataLink(models.Model):
    object_uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    parent_object_uid = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
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
# TODO: Single-choice / Select box


# Field
class Field(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    data_type = models.ForeignKey(DataType, on_delete=models.PROTECT)
    order = models.fields.IntegerField(default=0)

    def __str__(self):
        return self.object.__str__()
