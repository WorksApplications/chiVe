import argparse
from collections.abc import Iterable
from logging import INFO, basicConfig, getLogger
from pathlib import Path
from tqdm import tqdm

import sudachipy

basicConfig(
    format='%(levelname)s %(asctime)s [%(module)s:%(funcName)s:%(lineno)s] %(message)s', level=INFO)
logger = getLogger(__name__)


def parse_args():
    p = argparse.ArgumentParser(
        "Wakati-split given texts per line with A/B/C mode and normalized_form.")
    p.add_argument("--input", type=Path,
                   help="text file (line-by-line) or a directory contains them")
    p.add_argument("--output", type=Path,
                   help="directory to output")

    p.add_argument("--mode", type=str, default="ABC",
                   help="split mode to use (default: ABC)")
    p.add_argument("--skip-existing", action="store_true",
                   help="if set, skip processing if the output file already exists")

    args = p.parse_args()
    return args


def list_textfiles(input: Path) -> Iterable[Path]:
    """iterate over text files in the input directory (or input text file)"""
    if input.is_file():
        return [input]
    if input.is_dir():
        return input.glob("*.txt")
    return []


def mode2str(mode: sudachipy.SplitMode) -> str:
    """convert sudachipy.SplitMode into str"""
    match mode:
        case sudachipy.SplitMode.A: return "A"
        case sudachipy.SplitMode.B: return "B"
        case sudachipy.SplitMode.C: return "C"


def str2mode(modestr: str) -> sudachipy.SplitMode:
    """parse sudachipy.SplitMode from str"""
    match modestr.strip():
        case "A" | "a": return sudachipy.SplitMode.A
        case "B" | "b": return sudachipy.SplitMode.B
        case "C" | "c": return sudachipy.SplitMode.C
        case _: raise ValueError(f"cannot parse {modestr} as SplitMode.")


def output_filepath(input_file: Path, output_dir: Path, mode: sudachipy.SplitMode) -> Path:
    """generate output file path for the current input"""
    assert input_file.is_file()
    assert output_dir.is_dir()

    filename = f"{input_file.stem}_wakati_{mode2str(mode)}.txt"
    return output_dir / filename


def count_line(file: Path) -> int:
    """count line of a file"""
    assert file.is_file()
    with file.open() as fi:
        count = sum(1 for _ in fi)
    return count


def able_to_skip(infile: Path, outfile: Path) -> bool:
    """check if we can skip processing based on line count."""
    if not outfile.exists():
        return False

    lines_in = count_line(infile)
    lines_out = count_line(outfile)
    if lines_in == lines_out:
        return True
    return False


def wakati(tok: sudachipy.Tokenizer, sentence: str) -> str:
    """tokenize given sentence by the toknizer and return their normalized form joining with spaces."""
    morphemes = tok.tokenize(sentence)
    norm_forms = (m.normalized_form() for m in morphemes)
    return ' '.join(m for m in norm_forms if m != " ")


def wakati_file(infile: Path, outfile: Path, tok: sudachipy.Tokenizer) -> ():
    """apply wakati to each line of infile and write to outfile."""
    with infile.open() as fi, outfile.open("w") as fo:
        for line in tqdm(fi):
            line = line.strip()
            if line == "":
                fo.write("\n")
                continue
            fo.write(wakati(tok, line) + "\n")
    return


def main():
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    dic = sudachipy.Dictionary()
    for mode in map(str2mode, args.mode):
        tok = dic.create(mode=mode)
        for file in list_textfiles(args.input):
            outfile = output_filepath(file, args.output, mode)

            # check if skip
            if args.skip_existing and outfile.exists():
                if able_to_skip(file, outfile):
                    logger.info(
                        f"skip {file=} with split mode {mode2str(mode)}.")
                    continue
                logger.info(
                    f"{outfile=} exists but processing seems not finished.")

            # process
            logger.info(f"process {file=} with split mode {mode2str(mode)}.")
            logger.info(f"output file: \"{outfile}\"")
            wakati_file(file, outfile, tok)
    return


if __name__ == '__main__':
    main()
