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

def comparison(reference_file, generated_file, output_score_file):
    reference_summary = None
    with open(reference_file, "r") as file:
        reference_summary = file.read()

    generated_summary = None
    with open(generated_file, "r") as file:
        generated_summary = file.read()
    
    rouge_scores = calculate_rouge(reference_summary, generated_summary)
    bert_precision, bert_recall, bert_f1 = calculate_bertscore(reference_summary, generated_summary)

    with open(output_score_file, "w") as file:
        file.write("ROUGE Scores:\n")
        for metric, score in rouge_scores.items():
            file.write(f"{metric}: Precision={score.precision:.3f}, Recall={score.recall:.3f}, F1-Score={score.fmeasure:.3f}\n")
        file.write("\n")
        file.write("BERTScore:\n")
        file.write(f"Precision={bert_precision:.3f}, Recall={bert_recall:.3f}, F1-Score={bert_f1:.3f}\n")
    
