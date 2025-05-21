import pandas as pd
import dagster as dg
import clickhouse_connect
from datetime import datetime

from .config_ast import table_name, generate_case_id_from_run

def process_load(df: pd.DataFrame, table_name: str, case_id: int) -> pd.DataFrame:
    """
    주어진 DataFrame에 대해 로드 단계를 처리하고, 각 단계별 활동 로그(DataFrame)를 반환합니다.

    Args:
        df (pd.DataFrame): 처리할 원본 데이터
        table_name (str): 대상 테이블 이름
        case_id (int): 케이스 식별자

    Returns:
        pd.DataFrame: 활동 로그 데이터프레임
    """
    activity_logs = []
    input_count = len(df)

    # 적재 단계
    start_load = datetime.now()
    end_load = datetime.now()
    load_time = (end_load - start_load).total_seconds()

    activity_logs.append({
        'case_id': case_id,
        'table_name': table_name,
        'activity': 'load', # 동적으로 변경경
        'start_time': start_load,
        'end_time': end_load,
        'lead_time_sec': load_time,
        'status': 'SUCCESS',
        'remarks': f'{input_count} rows loaded'
    })

    return pd.DataFrame(activity_logs)

@dg.asset(
    group_name="data_selection",
    compute_kind="clickhouse-python",
    description="ClickHouse에서 조건에 따라 데이터를 조회하여 DataFrame으로 반환합니다."
    )
def get_dataframe_from_clickhouse(context: dg.AssetExecutionContext, table_name: str) -> None:
    """
    ClickHouse에서 조건에 따라 데이터를 조회하여 DataFrame으로 반환합니다.

    Args:
        table_name (str): 조회할 테이블 이름

    Returns:
        pd.DataFrame: 조회된 결과
    """
    # ClickHouse client 연결
    client = clickhouse_connect.get_client(
        host='localhost',       # 실제 서버 주소
        port=8123,
        username='default',
        password='',
        database='default'
    )
    query = f"SELECT * FROM {table_name}"

    # 쿼리 실행 후 DataFrame으로 반환
    df = client.query_df(query)
    
    # case_id 생성
    case_id = generate_case_id_from_run(context, table_name)
    
    # Activity: load 실행행
    df_log = process_load(df, table_name, case_id)
    
    context.add_output_metadata({
        "case_id": case_id,
        "log": dg.MetadataValue.md(df_log.to_markdown(index=False))
    })