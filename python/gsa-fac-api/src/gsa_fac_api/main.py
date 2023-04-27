import os
import typing
from typing import List, Set, Dict, Tuple

V0_URI="https://api.data.gov/TEST/audit-clearinghouse/v0/dissemination"

class FAC:
    def __init__(self, 
                 api_key=os.getenv("API_GOV_KEY"),
                 api_uri=V0_URI,
                 ):
        self.api_key = api_key
        self.api_uri = api_uri
        self._select = None
        self._table = None
    
    def select(self, list_of_columns : List[str]):
        self._select = list_of_columns
    
    def table(self, table : str):
        self._table = table

    def compose(self):
        url = ""
        url +   = self.api_uri
        if self._table is not None:
            url += f"/{self._table}"
        else:
            raise Exception("No table provided for FAC query.")

        query_params = []

        if self._select is not None:
            query_params.append(f"select={','.join(self._select)}")
        
        url += "?" + "&".join(query_params)
        
        return url