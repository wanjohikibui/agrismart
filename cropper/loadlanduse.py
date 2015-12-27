import os
from django.contrib.gis.utils import LayerMapping
from cropper.models import landuse

# Auto-generated `LayerMapping` dictionary for administration model
landuse_mapping = {
    'dn' : 'DN',
    'area' : 'Area',
    'landuse' : 'landuse',
    'geom' : 'MULTIPOLYGON',
}

mukurweini_landuse = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dss/data/mukurweini_landuse.shp'))

def run(verbose=True):
    lm = LayerMapping(landuse, mukurweini_landuse, landuse_mapping,transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)