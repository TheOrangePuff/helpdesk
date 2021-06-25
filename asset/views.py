from django.shortcuts import render
from . import forms
from . import models


def tree_diagram(request):
    template = 'asset/tree.html'

    # Get all the active objects
    objects = models.Object.objects.filter(active=True).values()

    return render(request, template, {'objects': objects})


def add(request, db_object):
    template = 'asset/add.html'

    if request.method == 'POST':
        form = forms.AddObjectData(data=request.POST, object_name=db_object)
        # check whether it's valid:
        if form.is_valid():
            # Save the form and return a blank form
            form.save()
            form = forms.AddObjectData(object_name=db_object)
    else:
        form = forms.AddObjectData(object_name=db_object)

    return render(request, template, {'form': form})
