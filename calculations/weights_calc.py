#Calculation to convert swing weights to normalised weights from Criteria

def normalise_weights(saved_weights):

    total_weight = sum(item["raw_weight"]
        for item in saved_weights.values()
    )

    if total_weight == 0:
        return {}

    return {

        criterion_id: {

            "criterion": item["criterion"],
            "raw_weight": item["raw_weight"],
            "normalised_weight": item["raw_weight"] / total_weight

        }

        for criterion_id, item
        in saved_weights.items()
    }