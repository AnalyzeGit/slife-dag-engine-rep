import dagster as dg
from dagster import MetadataValue
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from .nlp_config import FONT_DIR, IMAGE_DIR
from .text_processing import count_noun_frequency  # 의존성 명시

@dg.asset(
    group_name="visualization",
    compute_kind="python",
    deps=["count_noun_frequency"],  # 변경: 직접 count_noun_frequency에 의존
)
def visualize_noun_frequency(count_noun_frequency: pd.DataFrame):
    """명사 빈도 데이터를 사용하여 히스토그램을 생성하고 저장합니다 (함수 기반)."""
    # 현재 스크립트 위치 기준 폰트 경로
    font_path = FONT_DIR / "PRETENDARD-EXTRABOLD.OTF"
    fm.fontManager.addfont(font_path)
    plt.rc('font', family=fm.FontProperties(fname=font_path).get_name())
    plt.rcParams['axes.unicode_minus'] = False

    data = count_noun_frequency.sort_values(by='빈도', ascending=False).head(20)

    plt.figure(figsize=(12, 6))
    plt.bar(data['명사'], data['빈도'], color='orange')
    plt.xlabel("명사", fontsize=12)
    plt.ylabel("빈도", fontsize=12)
    plt.title(f"상위 20 명사 빈도 히스토그램", fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    plt.savefig(IMAGE_DIR / "noun_histogram.png")
    plt.close()  # 메모리 해제 (특히 반복 생성 시 필요)
    return dg.MaterializeResult(
        metadata={
            "plot_saved_to": str(IMAGE_DIR / "noun_histogram.png"),
            "plot": MetadataValue.md(f"![plot](file://{IMAGE_DIR / 'noun_histogram.png'})") 
            }
        )