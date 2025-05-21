from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESULT_DIR = DATA_DIR / "results"
FONT_DIR =  PROJECT_ROOT / "stats" / "fonts"
IMAGE_DIR = PROJECT_ROOT / "stats" / "images"

# 필요한 디렉토리 생성
for dir_path in [DATA_DIR, RESULT_DIR, FONT_DIR, IMAGE_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)