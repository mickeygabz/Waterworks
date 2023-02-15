from databricks import sql
import pandas as pd

host = 'adb-7292188950747655.15.azuredatabricks.net'
token = 'dapi27e78d7c5ed1b89249c06358486a4f0a-3'
http_path ='sql/protocolv1/o/7292188950747655/0927-050623-485kz8yt'

connection = sql.connect(server_hostname=host,  http_path= http_path,  access_token=token)
def get_data(query: str) -> pd.DataFrame:
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall_arrow().to_pandas()
    #cursor.close()
    #connection.close()
    return result
