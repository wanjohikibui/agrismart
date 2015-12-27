import os
from django.contrib.gis.utils import LayerMapping
from cropper.models import rainfall

# Auto-generated `LayerMapping` dictionary for administration model
rainfall_mapping = {
    'area' : 'AREA',
    'perimeter' : 'PERIMETER',
    'rainfall_field' : 'RAINFALL_',
    'rainfall_i' : 'RAINFALL_I',
    'type' : 'TYPE',
    'color' : 'COLOR',
    'geom' : 'MULTIPOLYGON',
}

mukurweini_rain = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dss/data/nyeri_rainfall.shp'))

def run(verbose=True):
    lm = LayerMapping(rainfall, mukurweini_rain, rainfall_mapping,transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)