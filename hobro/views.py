from django.shortcuts import render, get_object_or_404
from .models import *


def item_list(request):
    sections = Section.objects.order_by('time_stamp')
    #stories = Story.objects.order_by('time_stamp')
    items = []
    for s in sections:
        items.append(s)
    #for s in stories:
        #items.append(s)
    return render(request, 'hobro/item_list.html', {'items': items})


def item_detail(request, pk):
    item = get_object_or_404(Section, pk=pk)
    return render(request, 'hobro/item_detail.html', {'item': item})
