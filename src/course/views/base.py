from django.shortcuts import render
from course.models import subject
import collections


def render_with_default(request, template, context=None, **kwargs):
    default_context = {
         'active_subjects': subject.Subject.get_active()
    }
    return render(request, template, collections.ChainMap(context, default_context) if context is not None else default_context, **kwargs)