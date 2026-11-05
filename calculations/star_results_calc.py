
# ------- Total cost on Cost page ---------------------------------------------

def calculate_total_cost(
    cost_per_person,
    people_receiving
):

    try:
        cost_per_person = float(
            cost_per_person
        )
    except (TypeError, ValueError):
        cost_per_person = 0

    try:
        people_receiving = int(
            people_receiving
        )
    except (TypeError, ValueError):
        people_receiving = 0

    return round(
        cost_per_person * people_receiving,
        2
    )


# ------- Total benefit --------------------------------------------------------

def calculate_total_benefit(
    benefit_score,
    people_receiving
):

    try:
        benefit_score = float(
            benefit_score
        )
    except (TypeError, ValueError):
        benefit_score = 0

    try:
        people_receiving = int(
            people_receiving
        )
    except (TypeError, ValueError):
        people_receiving = 0

    return round(
        benefit_score * people_receiving,
        2
    )


# ------- VFM ratio ------------------------------------------------------------

def calculate_vfm_ratio(
    total_benefit,
    total_cost
):

    try:
        total_benefit = float(
            total_benefit
        )
    except (TypeError, ValueError):
        total_benefit = 0

    try:
        total_cost = float(
            total_cost
        )
    except (TypeError, ValueError):
        total_cost = 0

    # VFM cannot be calculated when Total Benefit is zero
    if total_benefit <= 0:
        return None

    return round(
        total_cost / total_benefit,
        2
    )


# ------- Add STAR-MCDA calculations to existing MCDA results -----------------

def calculate_star_results(
    results,
    costs
):

    star_results = []

    for result in results:

        option_id = result["option_id"]

        # Get saved cost information for this option
        cost_data = costs.get(
            option_id,
            {}
        )

        total_cost = float(
            cost_data.get(
                "total_cost",
                0
            )
        )

        people_receiving = int(
            cost_data.get(
                "people_receiving",
                0
            )
        )

        benefit_score = float(
            result.get(
                "benefit_score",
                0
            )
        )

        # Scale the Benefit Score by the number of people
        total_benefit = calculate_total_benefit(
            benefit_score,
            people_receiving
        )

        # Total Cost divided by Total Benefit
        vfm_ratio = calculate_vfm_ratio(
            total_benefit,
            total_cost
        )

        star_results.append({

            "option_id": option_id,

            "option": result["option"],

            "weighted_scores": result[
                "weighted_scores"
            ],

            # Original overall Benefit Score
            "benefit_score": benefit_score,

            # Number of people receiving the intervention
            "people_receiving": people_receiving,

            # STAR-MCDA totals
            "cost": total_cost,
            "total_benefit": total_benefit,

            # Cost per unit of Total Benefit
            "vfm_ratio": vfm_ratio
        })

    #------------------------------------------------------------------
    # STAR-MCDA ranking
    # Lower cost per unit of Total Benefit means better VFM


    star_results = sorted(
        star_results,
        key=lambda result: (
            result["vfm_ratio"] is None,
            result["vfm_ratio"]
            if result["vfm_ratio"] is not None
            else float("inf")
        )
    )

    # Add rank after every option has been processed
    for rank, result in enumerate(
        star_results,
        start=1
    ):

        result["rank"] = rank


    return star_results


# ------- Prepare efficiency-frontier data ------------------------------------

def calculate_efficiency_frontier(
    star_results
):

    # Lowest cost per unit of Total Benefit appears first
    ordered_results = sorted(
        star_results,
        key=lambda result: (
            result["vfm_ratio"] is None,
            result["vfm_ratio"]
            if result["vfm_ratio"] is not None
            else float("inf")
        )
    )

    frontier_results = []

    cumulative_cost = 0
    cumulative_benefit = 0

    for result in ordered_results:

        start_cost = cumulative_cost
        start_benefit = cumulative_benefit

        total_cost = float(
            result.get(
                "cost",
                0
            )
        )

        total_benefit = float(
            result.get(
                "total_benefit",
                0
            )
        )

        # Triangle base accumulates Total Cost
        cumulative_cost += total_cost

        # Triangle height accumulates Total Benefit
        cumulative_benefit += total_benefit

        frontier_results.append({

            "option_id": result["option_id"],

            "option": result["option"],

            "cost": total_cost,

            "benefit_score": float(
                result.get(
                    "benefit_score",
                    0
                )
            ),

            "people_receiving": int(
                result.get(
                    "people_receiving",
                    0
                )
            ),

            "total_benefit": total_benefit,

            "vfm_ratio": float(
                result.get(
                    "vfm_ratio",
                    0
                )
            ),

            "rank": result["rank"],

            "start_cost": start_cost,
            "start_benefit": start_benefit,

            "end_cost": cumulative_cost,
            "end_benefit": cumulative_benefit
        })

    return frontier_results
