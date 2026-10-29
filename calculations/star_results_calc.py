
#-------Total cost on cost pag calc-------------------------------------------

def calculate_total_cost(
    cost_per_person,
    people_receiving
):

    try:
        cost_per_person = float(cost_per_person)
    except:
        cost_per_person = 0

    try:
        people_receiving = int(people_receiving)
    except:
        people_receiving = 0

    return round(cost_per_person * people_receiving, 2)

#-------------VFM ratio cal------------------------------------------------------

def calculate_vfm_ratio(
    benefit_score,
    total_cost
):

    try:
        benefit_score = float(benefit_score)
    except (TypeError, ValueError):
        benefit_score = 0

    try:
        total_cost = float(total_cost)
    except (TypeError, ValueError):
        total_cost = 0

    # Avoid division by zero
    if benefit_score <= 0:
        return 0

    return round(
        total_cost / benefit_score,
        2
    )

#----------Add STAR-MCDA calculations to existing MCDA results--------------------------

def calculate_star_results(
    results,
    costs
):

    star_results = []

    for result in results:

        option_id = result["option_id"]

        # Get the saved cost record for this option
        cost_data = costs.get(option_id, {})

        # Total cost has already been calculated on the Cost page
        total_cost = cost_data.get("total_cost", 0)

        # Value For Money (VFM) ratio - calculating cost per unit of benefit
        vfm_ratio = calculate_vfm_ratio(result["benefit_score"], total_cost)

        star_results.append({

            "option_id": option_id,

            "option": result["option"],

            "weighted_scores": result["weighted_scores"],

            "cost": total_cost,

            "benefit_score": result["benefit_score"],

            "vfm_ratio": vfm_ratio

        })

        #-----STAR-MCDA ranking-----------
        # Lower cost per unit of benefit means better VFM

        star_results = sorted(star_results,
            key=lambda x: x["vfm_ratio"]
        )

        # Add rank after every option is added
        for rank, result in enumerate(
            star_results,
            start=1
        ):

            result["rank"] = rank


    return star_results


# ---------- Prepare efficiency frontier data ---------------------------------

def calculate_efficiency_frontier(star_results):

    # Lowest cost per unit of benefit represents better value for money,
    # so those interventions appear first.
    ordered_results = sorted(
        star_results,
        key=lambda result: result["vfm_ratio"]
    )

    frontier_results = []

    cumulative_cost = 0
    cumulative_benefit = 0

    for result in ordered_results:

        start_cost = cumulative_cost
        start_benefit = cumulative_benefit

        cumulative_cost += float(
            result.get("cost", 0)
        )

        cumulative_benefit += float(
            result.get("benefit_score", 0)
        )

        frontier_results.append({

            "option_id": result["option_id"],

            "option": result["option"],

            "cost": float(
                result.get("cost", 0)
            ),

            "benefit_score": float(
                result.get("benefit_score", 0)
            ),

            "vfm_ratio": float(
                result.get("vfm_ratio", 0)
            ),

            "rank": result["rank"],

            "start_cost": start_cost,
            "start_benefit": start_benefit,

            "end_cost": cumulative_cost,
            "end_benefit": cumulative_benefit
        })

    return frontier_results