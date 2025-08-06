import argparse, json
from discount_engine.allocator import allocate_discounts

def main():
    parser = argparse.ArgumentParser(description="Smart Discount Allocation Engine")
    parser.add_argument("--input", "-i", required=True, help="Path to input JSON file")
    parser.add_argument("--config", "-c", required=False, help="Path to config JSON file")
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        data = json.load(f)
    config = {}
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)

    result = allocate_discounts(data["siteKitty"], data["salesAgents"], config)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
