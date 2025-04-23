import argparse
from src.normalize import InverseTextNormalizer


def parse_args():
    parser = argparse.ArgumentParser(description="Inverse normalize text")
    parser.add_argument("input", type=str, help="input text")
    parser.add_argument("--verbose", action="store_true", help="print intermediate tokens")
    return parser.parse_args()

def main():
    args = parse_args()
    result = InverseTextNormalizer().inverse_normalize(args.input, args.verbose)
    print(result)

if __name__ == "__main__":
    main()