#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Author:zino

from django import template
register = template.Library()


@register.filter
def list(value):
    list = [1,6,10,11,12]
    if value in list:
        return value
    else:
        return None


@register.filter()
def product1(value):
    product1 = [1,2]
    if value in product1:
        return value

@register.filter()
def product2(value):
    product2 = [3]
    if value in product2:
        return value





