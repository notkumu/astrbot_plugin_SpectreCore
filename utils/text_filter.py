"""
文本过滤工具，用于清理大模型回复中的额外内容
"""
import sys

def filter_thinking_process(text: str) -> str:
    """
    过滤掉文本中被 <think></think> 标签包裹的思考过程内容
    
    Args:
        text: 输入文本
        
    Returns:
        过滤后的文本
    """
    if not text:
        return text
    
    try:
        # 检查文本开头是否有思考标签
        if text.startswith('<think>'):
            # 查找结束标签位置
            end_tag_pos = text.find('</think>')
            if end_tag_pos != -1:
                # 移除开头到</think>结束标签的内容
                return text[end_tag_pos + 8:].lstrip()  # 8是</think>的长度
                
        return text
    except Exception as e:
        print(f"过滤思考过程时出错: {e}", file=sys.stderr)
        # 出错时返回原始文本
        return text


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="过滤文本中的思考内容")
    parser.add_argument("-i", "--input", help="输入文件路径，默认为标准输入")
    parser.add_argument("-o", "--output", help="输出文件路径，默认为标准输出")
    args = parser.parse_args()
    
    # 处理输入
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as file:
                input_text = file.read()
        except Exception as e:
            print(f"读取输入文件错误: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("从标准输入读取文本（Ctrl+D 结束）：", file=sys.stderr)
        input_text = sys.stdin.read()
    
    # 处理文本
    filtered_text = filter_thinking_process(input_text)
    
    # 处理输出
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(filtered_text)
            print(f"过滤后的文本已写入: {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"写入输出文件错误: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(filtered_text) 