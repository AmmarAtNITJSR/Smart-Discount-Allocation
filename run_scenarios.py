#!/usr/bin/env python3
import json
import sys
from discount_engine.allocator import allocate_discounts

def main(input_path, config_path=None):
    # Load scenarios file
    data = json.load(open(input_path))
    # Load config once
    config = {}
    if config_path:
        config = json.load(open(config_path))
    # For each scenario, run allocation and print results
    for scenario in data.get("scenarios", []):
        print(f"\n=== Scenario: {scenario['name']} ===")
        result = allocate_discounts(
            scenario["siteKitty"],
            scenario["salesAgents"],
            config
        )
        print(json.dumps(result, indent=2))
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_scenarios.py testinput.json [config.json]")
    else:
        main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
