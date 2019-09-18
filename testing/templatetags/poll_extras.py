from django import template
from testing import models
import random


register = template.Library()


@register.filter(name='count_of_true_param')
def count_of_true_param(values, arg):
    count = 0
    for value in values:
        if getattr(value,arg):
            count += 1
    return count


@register.filter(name='is_finished')
def is_finished(test, user):
    result = models.Result.objects.all().filter(test=test, user=user).first()
    if result is None:
        return True
    else:
        return False


@register.filter
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp