#!/usr/bin/env python3

from argparse import ArgumentParser
import re
from datetime import date
from pathlib import Path
from subprocess import check_output
from typing import Dict, Generator, Iterable, Tuple
from warnings import warn


DATE_RE = r"(00?)\.(00?)\.(0000) ".replace("0", "[0-9]")


def grep_dates(pdfs: Iterable[Path]) -> Generator[Tuple[Path, date], None, None]:
    output = check_output(["pdfgrep", DATE_RE, *pdfs], encoding="utf-8")
    for grep_line in output.splitlines():
        filename, line = grep_line.split(":", 1)
        match = re.match(DATE_RE, line)
        if not match:
            warn("No date found on line: {grep_line.rstrip()}")
            continue
        year_str, month_str, day_str = reversed(match.groups())
        yield (Path(filename), date(int(year_str), int(month_str), int(day_str)))


def drop_multidate_pdfs(
    paths_and_dates: Iterable[Tuple[Path, date]]
) -> Dict[Path, date]:
    deduplicated: Dict[Path, date] = {}
    paths_with_duplicates = set()
    for path, date_obj in paths_and_dates:
        if path in deduplicated:
            del deduplicated[path]
            paths_with_duplicates.add(path)
        if path not in paths_with_duplicates:
            deduplicated[path] = date_obj
    return deduplicated


def add_date_to_filename(path: Path, date_obj: date) -> Path:
    iso_date = date_obj.strftime("%Y-%m-%d")
    if path.name.startswith(iso_date):
        return path
    return Path(path.parent / f"{iso_date} {path.name}")


def parse_directory_from_command_line() -> str:
    parser = ArgumentParser()
    parser.add_argument("directory", nargs="?", default=".")
    opts = parser.parse_args()
    return opts.directory


def main() -> None:
    directory = parse_directory_from_command_line()
    pdfs = Path(directory).glob("*.pdf")
    pdfs_and_dates = grep_dates(pdfs)
    one_date_pdfs = drop_multidate_pdfs(pdfs_and_dates)
    count_skipped, count_renamed = 0, 0
    for path, date_obj in one_date_pdfs.items():
        new_path = add_date_to_filename(path, date_obj)
        if new_path != path:
            print(f"Renaming {path.name!r} to {new_path.name!r}")
            path.rename(new_path)
            count_renamed += 1
        else:
            count_skipped += 1
    print(f"{count_renamed} PDF files renamed.")
    print(f"{count_skipped} PDF file names already have the correct date.")


if __name__ == "__main__":
    main()
