
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parkyou.models import *


def find_all_regulations(center, radius):
    #return list(Feature.objects(point__geo_within_sphere=[ center, radius ]).distinct( "sg_order_n"))
    return list(Feature.objects[:500])


def find_signs_for_regulation(reg):
    return list(Feature.objects( sg_order_n = reg))