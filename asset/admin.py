from django.contrib import admin
from . import models


@admin.register(models.Object)
class ObjectAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ObjectDataLink)
class ObjectDataLinkAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Data)
class ObjectData(admin.ModelAdmin):
    pass


@admin.register(models.ShortText)
class ObjectShortText(admin.ModelAdmin):
    pass


@admin.register(models.LongText)
class ObjectLongText(admin.ModelAdmin):
    pass


@admin.register(models.Boolean)
class ObjectBoolean(admin.ModelAdmin):
    pass


@admin.register(models.Image)
class ObjectImage(admin.ModelAdmin):
    pass


@admin.register(models.File)
class ObjectFile(admin.ModelAdmin):
    pass


@admin.register(models.Integer)
class ObjectInteger(admin.ModelAdmin):
    pass


@admin.register(models.PositiveInteger)
class ObjectPositiveInteger(admin.ModelAdmin):
    pass


@admin.register(models.Date)
class ObjectDate(admin.ModelAdmin):
    pass


@admin.register(models.Time)
class ObjectTime(admin.ModelAdmin):
    pass


@admin.register(models.DateTime)
class ObjectDateTime(admin.ModelAdmin):
    pass


@admin.register(models.SingleChoice)
class ObjectDateTime(admin.ModelAdmin):
    pass


@admin.register(models.Field)
class ObjectField(admin.ModelAdmin):
    pass
