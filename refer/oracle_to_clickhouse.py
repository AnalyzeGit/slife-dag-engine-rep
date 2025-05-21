# Oracle → ClickHouse 타입 매핑 테이블
oracle_to_clickhouse = {
    # 예시 매핑
    "VARCHAR2": "String",
    "CHAR": "String",
    "NUMBER": "Int64",
    "NUMBER(P)": "Int64",
    "NUMBER(P,S)": "Float64",
    "DATE": "Date",
    "TIMESTAMP": "DateTime",
    # ...여기에 직접 채워 넣으세요!
}

def normalize_oracle_type(oracle_type: str) -> str:
    """
    괄호 유무 및 자릿수에 따라 타입 키를 정리
    예: NUMBER(10,2) → NUMBER(P,S)
    """
    t = oracle_type.strip().upper()

    if t.startswith("NUMBER("):
        if "," in t:
            return "NUMBER(P,S)"
        else:
            return "NUMBER(P)"
    elif "(" in t:
        return t.split("(")[0]
    else:
        return t

def convert_tuple(column_name: str, nullable_flag: str, oracle_type: str) -> str:
    """
    컬럼 이름, NULL 여부, Oracle 타입 → ClickHouse 튜플 문자열로 변환
    """
    normalized = normalize_oracle_type(oracle_type)
    ck_type = oracle_to_clickhouse.get(normalized, "String")

    if nullable_flag.strip() == "":
        ck_type = f"Nullable({ck_type})"

    return f'("{column_name}", "{ck_type}")'

def convert_all(data_rows: list[tuple[str, str, str]]) -> list[str]:
    """
    전체 컬럼 정보를 리스트로 변환
    """
    return [convert_tuple(col, null, typ) for col, null, typ in data_rows]

input_data = [
    ("user_id", "", "VARCHAR2(50)"),
    ("amount", "", "NUMBER(10,2)"),
    ("qty", "Y", "NUMBER(8)"),
    ("registered_at", "Y", "DATE")
]

converted = convert_all(input_data)