def normalize(values):
    max_val = max(values) if values else 1
    if max_val == 0:
        max_val = 1
    return [v / max_val for v in values]

def distribute_leftover(allocations, scores, total_score, kitty):
    leftover = kitty - sum(allocations.values())
    if leftover <= 0:
        return allocations
    # sort ids by score descending
    sorted_ids = sorted(scores, key=lambda aid: scores[aid], reverse=True)
    i = 0
    while leftover > 0:
        aid = sorted_ids[i % len(sorted_ids)]
        allocations[aid] += 1
        leftover -= 1
        i += 1
    return allocations
