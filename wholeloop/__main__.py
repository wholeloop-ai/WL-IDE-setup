"""Allow `python -m wholeloop` when running from a checkout."""

from wholeloop.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
