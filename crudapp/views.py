from django.shortcuts import render, redirect, get_object_or_404

from .forms import ContactForm
from .models import Contact


def index_view(request):
    contacts = Contact.objects.all()

    context = {
        "contacts": contacts
    }

    # return render(request, 'crudapp/index.html', context)
    return render(request, 'crudapp/index.html', context)


def contact_details_view(request,pk):
    contact = get_object_or_404(Contact,pk=pk)
    context = {

    }
    return render(request, 'crudapp/contact-detail.html', context)


def create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = ContactForm()

    return render(request, 'crudapp/create.html', {'form': form})


def edit(request, pk, template_name='crudapp/edit.html'):
    contact = get_object_or_404(Contact, pk=pk)
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, template_name, {'form': form})


def delete(request, pk, template_name='crudapp/confirm_delete.html'):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('index')
    return render(request, template_name, {'object': contact})
