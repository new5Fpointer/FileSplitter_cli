import os
import re
import chardet

def log(message):
    """打印日志消息到控制台。"""
    print(f"[LOG] {message}")

def detect_encoding(file_path):
    """自动检测文件编码。"""
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)  # 读取前10000字节进行编码检测
        result = chardet.detect(raw_data)
        return result['encoding'] if result['confidence'] > 0.5 else 'utf-8'  # 如果置信度大于0.5，返回检测结果，否则默认为utf-8

def calculate_total_chars(input_path, encoding):
    """计算文件的总字符数。"""
    total_chars = 0
    with open(input_path, "r", encoding=encoding, errors="replace") as file:
        for line in file:
            total_chars += len(line)
    return total_chars

def ensure_dir_exists(dir_path):
    """确保目录存在，如果不存在则创建。"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def split_file_by_chars(input_path, output_dir, chars_per_file, input_encoding='auto', output_encoding='utf-8'):
    """按指定的字符数分割文件。"""
    log(f"开始按字符分割文件：{input_path}")
    if input_encoding == 'auto':
        input_encoding = detect_encoding(input_path)
    ensure_dir_exists(output_dir)  # 确保输出目录存在
    
    total_chars = calculate_total_chars(input_path, input_encoding)
    num_files = (total_chars + chars_per_file - 1) // chars_per_file
    
    with open(input_path, "r", encoding=input_encoding, errors="replace") as file:
        current_chars = 0
        file_index = 1
        current_chunk = []
        while True:
            line = file.readline()
            if not line:
                break
            line_length = len(line)
            if current_chars + line_length > chars_per_file:
                if current_chunk:
                    output_path = os.path.join(output_dir, f"part{file_index}.txt")
                    log(f"创建文件：{output_path}")
                    with open(output_path, "w", encoding=output_encoding, errors="replace") as out_file:
                        out_file.writelines(current_chunk)
                    file_index += 1
                    current_chars = 0
                    current_chunk = []
            current_chunk.append(line)
            current_chars += line_length
        
        if current_chunk:
            output_path = os.path.join(output_dir, f"part{file_index}.txt")
            log(f"创建文件：{output_path}")
            with open(output_path, "w", encoding=output_encoding, errors="replace") as out_file:
                 out_file.writelines(current_chunk)

def split_file_by_lines(input_path, output_dir, lines_per_file, input_encoding='auto', output_encoding='utf-8'):
    """按指定的行数分割文件。"""
    log(f"开始按行分割文件：{input_path}")
    if input_encoding == 'auto':
        input_encoding = detect_encoding(input_path)
    ensure_dir_exists(output_dir)  # 确保输出目录存在
    
    with open(input_path, "r", encoding=input_encoding, errors="replace") as file:
        current_lines = 0
        file_index = 1
        current_chunk = []
        while True:
            line = file.readline()
            if not line:
                break
            current_chunk.append(line)
            current_lines += 1
            if current_lines >= lines_per_file:
                output_path = os.path.join(output_dir, f"part{file_index}.txt")
                log(f"创建文件：{output_path}")
                with open(output_path, "w", encoding=output_encoding, errors="replace") as out_file:
                    out_file.writelines(current_chunk)
                file_index += 1
                current_chunk = []
                current_lines = 0
        
        if current_chunk:
            output_path = os.path.join(output_dir, f"part{file_index}.txt")
            log(f"创建文件：{output_path}")
            with open(output_path, "w", encoding=output_encoding, errors="replace") as out_file:
                 out_file.writelines(current_chunk)

def split_file_by_parts(input_path, output_dir, parts, input_encoding='auto', output_encoding='utf-8'):
    """按指定的份数分割文件。"""
    log(f"开始按份数分割文件：{input_path}")
    if input_encoding == 'auto':
        input_encoding = detect_encoding(input_path)
    ensure_dir_exists(output_dir)  # 确保输出目录存在
    
    total_chars = calculate_total_chars(input_path, input_encoding)
    chars_per_part = total_chars // parts
    remainder = total_chars % parts
    
    with open(input_path, "r", encoding=input_encoding, errors="replace") as file:
        for file_index in range(1, parts + 1):
            current_chunk_size = chars_per_part + (1 if file_index <= remainder else 0)
            chunk = ""
            while len(chunk) < current_chunk_size:
                line = file.readline()
                if not line:
                    break
                chunk += line
            output_path = os.path.join(output_dir, f"part{file_index}.txt")
            log(f"创建文件：{output_path} ({len(chunk)} 字符)")
            with open(output_path, "w", encoding=output_encoding, errors="replace") as out_file:
                out_file.write(chunk)

def split_file_by_regex(input_path, output_dir, regex_pattern, input_encoding='auto', output_encoding='utf-8', include_delimiter=False):
    """按正则表达式分割文件。"""
    log(f"开始按正则表达式分割文件：{input_path}")
    if input_encoding == 'auto':
        input_encoding = detect_encoding(input_path)
    ensure_dir_exists(output_dir)  # 确保输出目录存在
    
    pattern = re.compile(regex_pattern)
    with open(input_path, "r", encoding=input_encoding, errors="replace") as file:
        file_index = 1
        current_chunk = []
        for line in file:
            # 在当前行中查找所有匹配
            matches = list(pattern.finditer(line))
            
            if not matches:
                current_chunk.append(line)
                continue
            
            last_index = 0
            for match in matches:
                start, end = match.span()
                
                # 添加匹配前的部分
                if start > last_index:
                    current_chunk.append(line[last_index:start])
                
                # 处理匹配部分
                matched_text = line[start:end]
                
                # 如果当前块有内容，写入文件
                if current_chunk:
                    output_path = os.path.join(output_dir, f"part{file_index}.txt")
                    log(f"创建文件：{output_path}")
                    with open(output_path, "w", encoding=output_encoding, errors="replace") as out_file:
                        out_file.write(''.join(current_chunk))
                    file_index += 1
                    current_chunk = []
                
                # 是否包含分隔符在结果中
                if include_delimiter:
                    current_chunk.append(matched_text)
                last_index = end
                continue
            
            # 添加匹配后的剩余部分
            if last_index < len(line):
                current_chunk.append(line[last_index:])
        if current_chunk:
            output_path = os.path.join(output_dir, f"part{file_index}.txt")
            log(f"创建文件：{output_path}")
            with open(output_path, "w", encoding=output_encoding, errors="replace") as out_file:
                 out_file.write(''.join(current_chunk))
            file_index += 1
    
    # 写入最后一块
    if current_chunk:
        output_path = os.path.join(output_dir, f"part{file_index}.txt")
        log(f"创建文件：{output_path}")
        with open(output_path, "w", encoding=output_encoding, errors="replace") as out_file:
            out_file.write(''.join(current_chunk))