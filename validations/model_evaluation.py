from snowflake.snowpark.context import get_active_session
from utils.session import fetch_session
from rouge_score import rouge_scorer
import numpy as np
# Get the current session
try:
    session = get_active_session()
except Exception as e:
    print (str(e))
    session = fetch_session()

def compute_scores(row, score_type:str, metric_type:str):
    scorer = rouge_scorer.RougeScorer([score_type], use_stemmer=True)
    if row['MANUAL_DESCRIPTION'] and row['LLM_DESCRIPTION']:
        scores = scorer.score(row['MANUAL_DESCRIPTION'], row['LLM_DESCRIPTION'])
        precision, recall, fmeasure = scores[score_type]
        if metric_type == 'precision':
            return precision
        elif metric_type == 'recall':
            return recall
        elif metric_type == 'fmeasure':
            return fmeasure
    else:
        return np.nan

def evaluate_dataset(table_name:str):
    df = session.table(table_name)
    df_pandas = df.to_pandas()
    for score_type in ['rouge1', 'rouge2', 'rougeL']:
        df_pandas[score_type + '_precision'] = df_pandas.apply(compute_scores, args = (score_type, 'precision'), axis=1)
        df_pandas[score_type + '_recall'] = df_pandas.apply(compute_scores, args = (score_type, 'recall'), axis=1)
        df_pandas[score_type + '_fmeasure'] = df_pandas.apply(compute_scores, args = (score_type, 'fmeasure'), axis=1)
    return df_pandas

# Input the dataset/table in which we have reference text and LLM generated text
result_df = evaluate_dataset('LLM_MODEL_DATA_CATALOG')
result_df.to_csv("~/catalog_results.csv", index=False)