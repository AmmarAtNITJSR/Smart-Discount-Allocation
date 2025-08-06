def generate_justification(agent, amount, score, values):
    reasons = []
    perf, seni, targ, clients = agent["performanceScore"], agent["seniorityMonths"], agent["targetAchievedPercent"], agent["activeClients"]
    # Performance
    if perf >= max(values["performanceScore"]) * 0.9:
        reasons.append("excellent performance")
    elif perf >= max(values["performanceScore"]) * 0.75:
        reasons.append("good performance")
    # Seniority
    if seni >= max(values["seniorityMonths"]) * 0.9 and seni > 0:
        reasons.append("long-term contribution")
    elif seni <= max(values["seniorityMonths"]) * 0.2:
        reasons.append("recent onboarding")
    # Target achievement
    if targ >= max(values["targetAchievedPercent"]) * 0.9 and targ > 0:
        reasons.append("high target achievement")
    # Active clients
    if clients >= max(values["activeClients"]) * 0.9 and clients > 0:
        reasons.append("managing many clients")
    if not reasons:
        reasons.append("solid overall contribution")
    reasons[0] = reasons[0].capitalize()
    return " and ".join(reasons)
