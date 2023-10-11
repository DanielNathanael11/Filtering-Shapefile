from google.cloud import bigquery
import pandas as pd
import geopandas as gpd

json_key = 'C:/Users/Daniel Nathanael W/daniel-sa.json' # Change this into whatever your GCP service account is located
client = bigquery.Client.from_service_account_json(json_key)

query = """
select * except(snapshot_date, prc_date)
from ds_work.dsp_temp_shape_to_geojson
where wadmpr in ("Jawa Barat", "Jawa Tengah", "Jawa Timur")
"""

query_job = client.query(query)
df = query_job.to_dataframe()

df['geojson'] = gpd.GeoSeries.from_wkt(df['geojson'])
gdf = gpd.GeoDataFrame(df, geometry='geojson')
gdf.to_file('polygons.shp')