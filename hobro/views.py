from django.shortcuts import render
from .models import Section, Story


# Create your views here.
def item_list(request):
    sections = Section.objects.order_by('time_stamp')
    stories = Story.objects.order_by('time_stamp')
    items = []
    for s in sections:
        items.append(s)
    for s in stories:
        items.append(s)
    return render(request, 'hobro/item_list.html', {'items': items})


