import dagster as dg
import pandas as pd
from konlpy.tag import Okt
from collections import Counter
from pathlib import Path

from .memo_loader import load_raw_memo_data  # 수집 자산 임포트 (폴더 구조에 따라 조정)
from .nlp_config import RESULT_DIR  # nlp_config 폴더 위치에 따라 조정

@dg.asset(
    group_name="preprocessing",
    compute_kind="python",
    deps=["load_raw_memo_data"],
)
def extract_nouns_from_memo(load_raw_memo_data: pd.DataFrame) -> pd.DataFrame:
    """원시 메모 데이터에서 명사를 추출합니다."""
    okt = Okt()
    df = load_raw_memo_data.copy()
    df['nouns'] = df['memo'].apply(okt.nouns)
    df.to_csv(RESULT_DIR / "extracted_nouns_asset.csv", index=False)
    return df

@dg.asset(
    group_name="preprocessing",
    compute_kind="python",
    deps=["extract_nouns_from_memo"],
)
def count_noun_frequency(extract_nouns_from_memo: pd.DataFrame) -> pd.DataFrame:
    """추출된 명사의 빈도를 계산합니다."""
    all_nouns = [noun for sublist in extract_nouns_from_memo['nouns'] for noun in sublist]
    noun_frequency = Counter(all_nouns)
    freq_df = pd.DataFrame(noun_frequency.items(), columns=['명사', '빈도']).sort_values(by='빈도', ascending=False)
    return freq_df