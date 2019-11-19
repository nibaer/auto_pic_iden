from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
import math
import sys

# Create your views here.
@api_view(["POST"])
def IdealWeight(rgb16):
    try:
        result = color_similarity(rgb16.body)
        return JsonResponse(result, safe=False)
    except ValueError as e:
        print(rgb16.body)
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)


red_rgb = '#FF0000'
orange_rgb = '#FFA500'
yello_rgb = '#FFFF00'
green_rgb = '#00FF00'
turquoise_rgb = '#40E0D0'
blue_rgb= '#0000FF'
purple_rgb = '#800080'
white_rgb = '#FFFFFF'
black_rgb = '#000000'


def color_similarity(target_color):
    ref_colors = [red_rgb, orange_rgb, yello_rgb, green_rgb, turquoise_rgb, blue_rgb, purple_rgb, white_rgb, black_rgb]

    color_sim_float = []
    for a_ref_color in ref_colors:
        sim_value = calc_sim_value(target_color, a_ref_color)
        color_sim_float.append(sim_value)

    sim_probability=[sim_value/sum(color_sim_float) for sim_value in color_sim_float]

    color_sim = [ "%2d"%(sim_prob*100)+"%" for sim_prob in sim_probability]

    result = '"red_v":"{0}", "orange_v":"{1}", "yellow_v":"{2}", "green_v":"{3}" ' + \
             ', "turquoise_v":"{4}" , "blue_v":"{5}", "purple_v":"{6}", "white_v":"{7}", "black_v":"{8}"'
    result = result.format(color_sim[0], color_sim[1], color_sim[2], color_sim[3], color_sim[4], color_sim[5], \
                           color_sim[6], color_sim[7], color_sim[8])
    result = '{' + result + '}'
    print(result)
    return result


def calc_sim_value(target_color, a_ref_color):
    tgt = rgb_list(target_color)
    ref = rgb_list(a_ref_color)
    #distance=math.sqrt((math.pow(tgt[0]-ref[0], 2)+math.pow(tgt[1]-ref[1], 2)+math.pow(tgt[2]-ref[2], 2))/3)
    distance=(math.pow(tgt[0]-ref[0], 2)+math.pow(tgt[1]-ref[1], 2)+math.pow(tgt[2]-ref[2], 2))/3
    if distance ==0:
        sim = sys.maxsize
    else:
        sim =1/distance
    return sim


def rgb_list(hex_color):
    red_value = int(hex_color[1:3], 16)
    green_value = int(hex_color[3:5], 16)
    blue_value = int(hex_color[5:7], 16)
    return [red_value, green_value, blue_value]