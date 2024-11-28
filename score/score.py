from rouge_score import rouge_scorer
from bert_score import score

### 1. ROUGE score
def calculate_rouge(reference, generated):

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)
    return scores

### 2.BERTScore
def calculate_bertscore(reference, generated):

    P, R, F1 = score([generated], [reference], lang="en", verbose=True)
    return P[0].item(), R[0].item(), F1[0].item()