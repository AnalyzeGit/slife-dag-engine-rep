import pandas as pd
import clickhouse_connect

def load_clickhouse_table(database: str, table_name: str, data: pd.DataFrame) -> None:
    """
    pandas DataFrame을 ClickHouse 테이블에 적재합니다.
    (테이블은 미리 존재한다고 가정합니다)

    Args:
        database (str): ClickHouse 데이터베이스 이름
        table_name (str): 테이블 이름
        data (pd.DataFrame): 삽입할 데이터프레임

    Returns:
        None
    """

    # ClickHouse 접속 정보
    client = clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='default',
        password='',  # 기본 사용자이므로 비어 있을 수 있음
        database=database
    )

    try:
        if not data.empty:
            client.insert_df(f'{database}.{table_name}', data)
            print(f'DataFrame successfully loaded into {table_name} in ClickHouse.')
        else:
            print("The DataFrame is empty. No data loaded.")

    except Exception as e:
        print(f"Failed to load data to ClickHouse: {e}")


# 테스트용 데이터프레임 생성
test_df = pd.DataFrame({
    'event_id': [1001, 1002, 1003],
    'user_id': [501, 502, 503]
})

load_clickhouse_table('default', 'user_events', test_df)