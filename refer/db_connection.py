import clickhouse_connect

class ClickHouseConnectionTester:
    def __init__(self, host='localhost', port=8123, username='default', password='', database='default'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def test_connection(self):
        try:
            client = clickhouse_connect.get_client(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                database=self.database
            )
            # 서버에 Ping 요청
            client.ping()
            print("✅ ClickHouse 연결 성공!")
            return True
        except Exception as e:
            print(f"❌ ClickHouse 연결 실패: {e}")
            return False

if __name__ == "__main__":
    tester = ClickHouseConnectionTester(
        host='10.29.50.57',
        port=8123,
        username='pduser',
        password='rhtmxm',
        database='prodiscovery'
    )
    tester.test_connection()
