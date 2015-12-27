import os
from django.contrib.gis.utils import LayerMapping
from cropper.models import temperature

# Auto-generated `LayerMapping` dictionary for administration model
temperature_mapping = {
    'area' : 'AREA',
    'perimeter' : 'PERIMETER',
    'temptra_field' : 'TEMPTRA_',
    'temptra_id' : 'TEMPTRA_ID',
    'tem' : 'TEM',
    'temrate' : 'TEMRATE',
    'avg' : 'AVG',
    'geom' : 'MULTIPOLYGON',
}


mukurweini_temp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dss/data/temperature.shp'))

def run(verbose=True):
    lm = LayerMapping(temperature, mukurweini_temp, temperature_mapping,transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)