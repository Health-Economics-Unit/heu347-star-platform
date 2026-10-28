# Results summary, decision matrix and visualisation chart

def calculate_results(scores, weights):

    results = []

    for option_id, option_data in scores.items():

        weighted_scores = {}

        total_benefit_score = 0

        for criterion_id, criterion_data in option_data["criteria_scores"].items():

            score = criterion_data["score"]

            weight = weights[criterion_id]["normalised_weight"]
            weighted_score = score * weight

            weighted_scores[criterion_data["criterion"]] = round(weighted_score, 2)

            total_benefit_score += weighted_score

        results.append({

            "option_id": option_id,

            "option": option_data["option"],

            "weighted_scores": weighted_scores,

            "benefit_score": round(total_benefit_score, 2)

        })

#--------- ranking option---------------------------------------------------------------------

    results = sorted(
        results,
        key=lambda x: x["benefit_score"],
        reverse=True
    )

    for rank, result in enumerate(
        results,
        start=1
    ):

        result["rank"] = rank

    return results

