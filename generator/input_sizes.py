# Single source of truth for benchmark input sizes.
# Frontend sends only: small | medium | large.
INPUT_SIZES = {
    "small": 1000,
    "medium": 10000,
    "large": 100000,
}

def get_input_size(size: str) -> int:
    size = size.lower().strip()
    if size not in INPUT_SIZES:
        raise ValueError(f"Unsupported input size: {size}")
    return INPUT_SIZES[size]
