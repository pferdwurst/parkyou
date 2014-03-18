
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parkyou.models import *


def find_all_regulations():
    return list(Feature.objects.distinct( "sg_order_n"))


def find_signs_for_regulation(reg):
    return list(Feature.objects( sg_order_n = reg))