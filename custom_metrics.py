def accuracy(number_of_correct, number_of_examples):
    return number_of_correct / number_of_examples


def compute_squad_metrics(predictions, references):
    """
    Computes SQuAD metrics, maximizing over answers per question.

    Args:
        predictions (dict): Predicted answers for each question in the SQuAD dataset.
                            The dictionary should have question IDs as keys and predicted answers as values.
        references (dict): Ground truth answers for each question in the SQuAD dataset.
                           The dictionary should have question IDs as keys and reference answers as values.

    Returns:
        float: Exact Match (EM) score
        float: F1 score
    """
    em_score = 0  # Exact Match (EM) score
    f1_score = 0  # F1 score

    for question_id, predicted_answer in predictions.items():
        reference_answer = references.get(question_id, "")

        em_score += exact_match_score(predicted_answer, reference_answer)
        f1_score += f1_score_compute(predicted_answer, reference_answer)

    num_questions = len(predictions)
    em_score /= num_questions
    f1_score /= num_questions

    return em_score, f1_score


def exact_match_score(prediction, reference):
    """
    Computes the Exact Match (EM) score between a predicted answer and a reference answer.

    Args:
        prediction (str): Predicted answer
        reference (str): Reference answer

    Returns:
        float: Exact Match (EM) score
    """
    return float(prediction.lower() == reference.lower())


def f1_score_compute(prediction, reference):
    """
    Computes the F1 score between a predicted answer and a reference answer.

    Args:
        prediction (str): Predicted answer
        reference (str): Reference answer

    Returns:
        float: F1 score
    """
    prediction_tokens = prediction.lower().split()
    reference_tokens = reference.lower().split()

    common_tokens = set(prediction_tokens) & set(reference_tokens)
    num_common_tokens = len(common_tokens)

    if num_common_tokens == 0:
        return 0

    precision = num_common_tokens / len(prediction_tokens)
    recall = num_common_tokens / len(reference_tokens)

    f1_score = (2 * precision * recall) / (precision + recall)

    return f1_score
