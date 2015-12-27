import os
from django.contrib.gis.utils import LayerMapping
from cropper.models import soil

# Auto-generated `LayerMapping` dictionary for administration model
soil_mapping = {
    'phaq' : 'PHAQ',
    'drai_descr' : 'DRAI_DESCR',
    'slop' : 'SLOP',
    'text' : 'TEXT',
    'text_descr' : 'TEXT_DESCR',
    'rslo_descr' : 'RSLO_DESCR',
    'geom' : 'MULTIPOLYGON',
}

mukurweini_soil = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dss/data/soil_data.shp'))

def run(verbose=True):
    lm = LayerMapping(soil, mukurweini_soil, soil_mapping,transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)