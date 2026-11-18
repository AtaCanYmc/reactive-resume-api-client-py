"""Output formatters for CLI."""

import json
from typing import Any


def format_json(data: Any) -> str:
    """Format data as pretty-printed JSON."""
    if hasattr(data, "model_dump"):
        data = data.model_dump(mode="json", exclude_none=True)
    elif isinstance(data, list) and data and hasattr(data[0], "model_dump"):
        data = [item.model_dump(mode="json", exclude_none=True) for item in data]
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """Print tabular data using Rich if available, or simple stdlib fallback."""
    try:
        from rich.console import Console
        from rich.table import Table

        table = Table(show_header=True, header_style="bold cyan")
        for h in headers:
            table.add_column(h)
        for row in rows:
            table.add_row(*[str(cell if cell is not None else "") for cell in row])
        Console().print(table)
    except ImportError:
        # Fallback table formatting without external dependencies
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell if cell is not None else "")))

        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        sep_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
        print(header_line)
        print(sep_line)
        for row in rows:
            print(
                " | ".join(
                    str(cell if cell is not None else "").ljust(col_widths[i])
                    for i, cell in enumerate(row)
                )
            )
