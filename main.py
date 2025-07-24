import argparse
import os
from core.splitter import split_file_by_chars, split_file_by_lines, split_file_by_parts, split_file_by_regex

def cli_main():
    parser = argparse.ArgumentParser(description="文件分割工具 - 命令行版")
    parser.add_argument("-i", "--input", required=True, help="输入文件路径")
    parser.add_argument("-o", "--output", required=True, help="输出目录")
    parser.add_argument("-m", "--mode", default="chars", choices=["chars", "lines", "parts", "regex"], help="分割模式：chars(字符) | lines(行) | parts(份数) | regex(正则)")
    parser.add_argument("-s", "--size", type=int, default=1000, help="字符数/行数/份数(取决于 -m)")
    parser.add_argument("--in-enc", default="auto", help="输入文件编码，默认 auto")
    parser.add_argument("--out-enc", default="utf-8", help="输出文件编码，默认 utf-8")
    parser.add_argument("--regex", default="", help="正则表达式(仅在 -m regex 时有效)")
    parser.add_argument("--include-delimiter", action="store_true", help="正则分割时是否包含分隔符")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print("错误：输入文件不存在")
        return

    if args.mode == "chars":
        split_file_by_chars(args.input, args.output, args.size, args.in_enc, args.out_enc)
    elif args.mode == "lines":
        split_file_by_lines(args.input, args.output, args.size, args.in_enc, args.out_enc)
    elif args.mode == "parts":
        split_file_by_parts(args.input, args.output, args.size, args.in_enc, args.out_enc)
    elif args.mode == "regex":
        if not args.regex:
            print("错误：正则模式必须提供 --regex 参数")
            return
        split_file_by_regex(args.input, args.output, args.regex, args.in_enc, args.out_enc, args.include_delimiter)

    print("完成！")

if __name__ == "__main__":
    cli_main()