#This page will perform all calculations

def calculate_option_score(
    clinical,
    inequalities,
    deliverability,
    clinical_weight,
    inequalities_weight,
    deliverability_weight
):

    return (

        clinical * clinical_weight +

        inequalities * inequalities_weight +

        deliverability * deliverability_weight

    )


def calculate_weighted_score(
    score,
    weight
):

    return score * weight


def calculate_total_score(
    scores
):

    return sum(scores)
