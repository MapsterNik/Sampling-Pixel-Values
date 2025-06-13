import ee
import geemap

ee.Authenticate()
ee.Initialize(project = 'ee-my-nikhil')

roi = ee.FeatureCollection("FAO/GAUL/2015/level1")\
      .filter(ee.Filter.eq('ADM1_NAME', 'Tamil Nadu'))

dem = ee.Image("USGS/SRTMGL1_003")\
      .clip(roi)

s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")\
    .filterDate('2024', '2025')\
    .filterBounds(roi)\
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))\
    .select(['B.*'])

def scaling(image):
  return image.multiply(0.0001)

image = s2.map(scaling).median().clip(roi)

randPoints = roi.randomPoints(region = roi, points = 50, seed = 5)

samplingDem = dem.sampleRegions(randPoints, ['Elevation'], 30)
samplingS2 = image.sample(randPoints, 10)

m = geemap.Map(toolbar_ctrl = True, draw_ctrl = False, basemap = 'SATELLITE', search_ctrl = False, measure_ctrl  = False,
               layer_ctrl = True)

viz_params = {'min': 0, 
              'max': 400,
              'palette': ["006633", "E5FFCC", "662A00", "D8D8D8", "F5F5F5"]
}

m.add_layer(image, {
    'min': 0, 'max': 0.3,
    'bands': ['B4', 'B3', 'B2']
}, 'Sentinel 2')

m.add_layer(dem, viz_params, 'DEM');

m.add_layer(roi.style(**{
    'color': 'black',
    'fillColor': 'ffffff00'
}), {}, 'Tamilnadu')

m.add_layer(randPoints.style(**{
    'color': 'red',
    'pointSize': 3
}), {}, 'Random Points')

m.add_colorbar(viz_params, label = 'Elevation')

m.centerObject(roi, 7)