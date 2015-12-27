import os
from django.contrib.gis.utils import LayerMapping
from cropper.models import ph

# Auto-generated `LayerMapping` dictionary for administration model
ph_mapping = {
    'phaq' : 'PHAQ',
    'geom' : 'MULTIPOLYGON',
}


mukurweini_ph = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dss/data/ph.shp'))

def run(verbose=True):
    lm = LayerMapping(ph, mukurweini_ph, ph_mapping,transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)