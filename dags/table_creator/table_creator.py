import clickhouse_connect

class ClickHouseConnectionTester:
    def __init__(self, host='localhost', port=8123, username='default', password='', database='default') -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def _create_clickhouse_connection(self) -> None:
        try:
            self._client = clickhouse_connect.get_client(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                database=self.database
            )
            # 서버에 Ping 요청
            self._client.ping()
            print("✅ ClickHouse 연결 성공!")

        except Exception as e:
            print(f"❌ ClickHouse 연결 실패: {e}")

    def _format_columns(self, columns: list) -> str:
        max_len = max(len(name) for name, _ in columns)
        indent = " " * 4  # 4칸 들여쓰기
        return ",\n".join(
            f"{indent}{name.ljust(max_len)} {dtype}" for name, dtype in columns
        )

    def create_clickhouse_connection(self, table_name: str, columns: list, engine: str="MergeTree", order_by: str=None):
        # 클릭하우스 연결 파악
        self._create_clickhouse_connection()

        if not columns:
            raise ValueError("columns 리스트가 비어 있습니다.")
        
        # column_defs = ",\n    ".join([f"{name} {dtype}" for name, dtype in columns])
        column_defs = self._format_columns(columns)
        order_clause = order_by or columns[0][0] 

        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {column_defs}
        )
        ENGINE = {engine} 
        ORDER BY {order_clause}
        """
        self._client.command(query)

if __name__ == "__main__":
    # tester = ClickHouseConnectionTester(
    #     host='10.29.50.57',
    #     port=8123,
    #     username='pduser',
    #     password='rhtmxm',
    #     database='prodiscovery'
    # )
    tester = ClickHouseConnectionTester(
        host='localhost',
        port=8123,
        username='default',
        password='',
        database='default'
    )
    # 예시
    table_name = "user_events"
    columns = [
        ("event_id", "UInt64"),
        ("user_id", "UInt32")
    ]
    tester.create_clickhouse_connection(table_name, columns)
