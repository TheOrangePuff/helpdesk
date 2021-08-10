from django.shortcuts import render, redirect
from django.forms import modelformset_factory
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


def view(request, db_object):
    template = 'asset/view.html'

    object_data_links = models.ObjectDataLink.objects.filter(object=db_object)

    object_list = []
    for data in object_data_links:
        # TODO: add a link for choice fields to display the selected data in full
        #       e.g click the laptop serial number to go to asset/view/laptop/uid
        object_list.append(data.get_data())

    return render(request, template, {'object_list': object_list})


def create(request):
    template = 'asset/create.html'

    if request.method == 'POST':
        form = forms.ObjectCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Save the form and return a blank form
            form.save()
            form = forms.ObjectCreationForm()
    else:
        form = forms.ObjectCreationForm()

    return render(request, template, {'form': form})


def edit(request, db_object):
    template = 'asset/edit.html'
    fields = ('name', 'friendly_name', 'desc', 'data_type', 'friendly_field')
    field_forms = modelformset_factory(models.Field,
                                       fields=fields,
                                       formset=forms.FieldCreationFormSet)
    queryset = models.Field.objects.filter(parent_object=db_object)

    if request.method == 'POST':
        formset = field_forms(request.POST, queryset=queryset)
        # check whether it's valid:
        for form in formset:
            if form.is_valid():
                # Save the form and return a blank form
                form.save()
                return redirect(create)
    else:
        formset = field_forms(request.POST, queryset=queryset)

    return render(request, template, {'formset': formset})
