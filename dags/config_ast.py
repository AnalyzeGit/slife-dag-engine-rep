import pandas as pd
import dagster as dg
import clickhouse_connect
from datetime import datetime

@dg.asset(
    group_name="data_selection",
    compute_kind="python",
    description="ClickHouse에서 조회할 테이블명을 정의합니다."
)
def table_name(context: dg.AssetExecutionContext) -> str:
    value = "user_events"
    context.log.info(f"[table_name] 반환 값: {value}")
    context.add_output_metadata({
        "table_name": dg.MetadataValue.text(value)
        }
    )
    return value

def generate_case_id_from_run(context: dg.AssetExecutionContext, table_name: str) -> str:
    run_base = context.run_id[:8]
    return f"{table_name}_{run_base}"