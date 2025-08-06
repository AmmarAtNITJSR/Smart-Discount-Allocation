import math
from .justification import generate_justification
from .utils import normalize, distribute_leftover

def allocate_discounts(site_kitty, sales_agents, config=None):
    config = config or {}
    weights = config.get("weights", {
        "performanceScore": 1.0,
        "seniorityMonths": 1.0,
        "targetAchievedPercent": 1.0,
        "activeClients": 1.0
    })
    # percentages to amounts
    min_alloc = config.get("min_allocation_amount", 0)
    max_alloc = config.get("max_allocation_amount", float('inf'))
    if config.get("min_allocation_percent"):
        min_alloc = max(min_alloc, config["min_allocation_percent"] * site_kitty)
    if config.get("max_allocation_percent"):
        max_alloc = min(max_alloc, config["max_allocation_percent"] * site_kitty)

    use_base = config.get("use_base_allocation", False)
    base_percent = config.get("base_allocation_percent", 0.0)

    n = len(sales_agents)
    allocations = {agent['id']: 0 for agent in sales_agents}

    # Base allocation
    base_total = base_percent * site_kitty if use_base else 0
    if base_total and n:
        base_each = base_total / n
        for agent in sales_agents:
            allocations[agent['id']] = base_each
    remaining = site_kitty - (base_total if use_base else 0)

    # Compute normalized scores
    attrs = ["performanceScore", "seniorityMonths", "targetAchievedPercent", "activeClients"]
    values = {attr: [agent[attr] for agent in sales_agents] for attr in attrs}
    norms = {attr: normalize(vals) for attr, vals in values.items()}

    scores = {}
    for idx, agent in enumerate(sales_agents):
        score = sum(weights[attr] * norms[attr][idx] for attr in attrs)
        scores[agent['id']] = score

    total_score = sum(scores.values())
    if total_score > 0:
        for agent in sales_agents:
            share = scores[agent['id']] / total_score
            allocations[agent['id']] += share * remaining
    else:
        # equal split if no score
        for agent in sales_agents:
            allocations[agent['id']] += remaining / n if n else 0

    # Enforce min/max iteratively
    changed = True
    while changed:
        changed = False
        for agent in sales_agents:
            aid = agent['id']
            amt = allocations[aid]
            if amt < min_alloc:
                diff = min_alloc - amt
                allocations[aid] = min_alloc
                per_other = diff / (n - 1)
                for other in sales_agents:
                    if other['id'] != aid:
                        allocations[other['id']] -= per_other
                changed = True
                break
            if amt > max_alloc:
                diff = amt - max_alloc
                allocations[aid] = max_alloc
                per_other = diff / (n - 1)
                for other in sales_agents:
                    if other['id'] != aid:
                        allocations[other['id']] += per_other
                changed = True
                break

    # Rounding
    for aid in allocations:
        allocations[aid] = math.floor(allocations[aid])
    allocations = distribute_leftover(allocations, scores, total_score, site_kitty)

    # Build output
    output = {"allocations": []}
    for agent in sales_agents:
        aid = agent['id']
        output["allocations"].append({
            "id": aid,
            "assignedDiscount": int(allocations[aid]),
            "justification": generate_justification(agent, allocations[aid], scores[aid], values)
        })
    return output
