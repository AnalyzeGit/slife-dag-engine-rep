from dagster import Definitions

from .load_ast import get_dataframe_from_clickhouse
from .config_ast import table_name

defs = Definitions(
    assets =[table_name, get_dataframe_from_clickhouse],
)