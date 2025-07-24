#!/usr/bin/env python3
import argparse
import os
import sys
from core.splitter import (
    split_file,
    split_file_by_lines,
    split_file_by_parts,
    split_file_by_regex,
)

def log(msg):
    print(msg, flush=True)

def cli_main():
    p = argparse.ArgumentParser(description="File Splitter CLI")
    p.add_argument("-i", "--input", required=True, help="input file")
    p.add_argument("-o", "--output", required=True, help="output folder")
    p.add_argument("-m", "--mode", default="chars",
                   choices=["chars", "lines", "parts", "regex"])
    p.add_argument("-s", "--size", type=int, default=1000,
                   help="chars / lines / parts")
    p.add_argument("--in-enc", default="auto")
    p.add_argument("--out-enc", default="utf-8")
    p.add_argument("--regex", default="", help="regex pattern")
    p.add_argument("--include-delimiter", action="store_true")
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)

    if args.mode == "chars":
        split_file(args.input, args.output, args.size,
                   args.in_enc, args.out_enc)
    elif args.mode == "lines":
        split_file_by_lines(args.input, args.output, args.size,
                            args.in_enc, args.out_enc)
    elif args.mode == "parts":
        split_file_by_parts(args.input, args.output, args.size,
                            args.in_enc, args.out_enc)
    elif args.mode == "regex":
        if not args.regex:
            print("缺少 --regex", file=sys.stderr); sys.exit(1)
        split_file_by_regex(args.input, args.output, args.regex,
                            args.in_enc, args.out_enc,
                            include_delimiter=args.include_delimiter)
    print("✅ 完成！")

if __name__ == "__main__":
    cli_main()