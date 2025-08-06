# Smart Discount Allocation Engine

This project is a Python CLI tool to allocate a discount kitty among sales agents based on configurable, data-driven logic.

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```bash
python cli.py --input sample_input.json --config config.json
python cli.py --input testinput1.json --config config.json
python cli.py --input testinput2.json --config config.json
python cli.py --input testinput3.json --config config.json
```

## Structure
- `cli.py`: Main CLI entrypoint.
- `discount_engine/allocator.py`: Core allocation logic.
- `discount_engine/justification.py`: Justification text generation.
- `discount_engine/utils.py`: Utility functions for normalization and rounding.
- `config.json`: Example configuration file.
- `tests/`: Unit tests for allocation logic.
