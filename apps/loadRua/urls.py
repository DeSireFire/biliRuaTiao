# coding=utf8
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5 0:11
# @Author  : RaXianch
# @project: biliRuaTiao.py
# @FileName: urls.py
# @Software: PyCharm
# @github    ：https://github.com/DeSireFire

from django.urls import path
from .views import *
urlpatterns = [
    path('', index),
]