import os
from django.contrib.gis.utils import LayerMapping
from cropper.models import elevation

# Auto-generated `LayerMapping` dictionary for administration model
elevation_mapping = {
    'id' : 'ID',
    'elev' : 'ELEV',
    'geom' : 'MULTILINESTRING',
}


mukurweini_elev = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dss/data/contours.shp'))

def run(verbose=True):
    lm = LayerMapping(elevation, mukurweini_elev, elevation_mapping,transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)