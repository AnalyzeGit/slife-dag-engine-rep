import dagster as dg
import pandas as pd
from pathlib import Path

from .nlp_config import DATA_DIR

@dg.asset(
    group_name="ingestion",
    compute_kind="python",
)
def load_raw_memo_data() -> pd.DataFrame:
    """메모 데이터를 CSV 파일에서 로드합니다."""
    data_path = DATA_DIR / 'memo.csv'
    df = pd.read_csv(data_path)
    return df

@dg.asset_check(
    asset=load_raw_memo_data
)
def memo_data_file_exists_check(context) -> dg.AssetCheckResult:
    """'memo.csv' 파일이 데이터 디렉토리에 존재하는지 검사합니다."""
    data_path = DATA_DIR / 'memo.csv'
    file_exists = data_path.exists()
    return dg.AssetCheckResult(
        passed=file_exists,
        metadata={
            "file_path": dg.MetadataValue.text(str(data_path))
        }
    )
