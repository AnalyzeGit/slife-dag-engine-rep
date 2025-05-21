from dagster import Definitions

from .assets.memo_loader import load_raw_memo_data, memo_data_file_exists_check
from .assets.text_processing import extract_nouns_from_memo, count_noun_frequency
from .assets.noun_frequency_histogram import visualize_noun_frequency

defs = Definitions(
    assets=[load_raw_memo_data, extract_nouns_from_memo, count_noun_frequency, visualize_noun_frequency],
    asset_checks=[memo_data_file_exists_check],
) 


