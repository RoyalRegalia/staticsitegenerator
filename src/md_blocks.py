from enum import Enum

#alternative version because I had formatted testing wrong, had to clean extra white space here there everywhere (curse tabbing)
##def markdown_to_blocks(markdown):
#    md_block_lst = []
#    blocks = markdown.split("\n\n")
#    for block in blocks:
#        block = block.strip()
#        if block != "":
#            lines = block.splitlines() #separated into lines with \n
#            cleaned_lines = []
#            for line in lines: #for each line to be cleaned
#                cleaned_lines.append(line.strip()) #stripped of white space
#            cleaned_block = "\n".join(cleaned_lines)
#            md_block_lst.append(cleaned_block)
#    return md_block_lst

def markdown_to_blocks(markdown):
    md_block_lst = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        md_block_lst.append(block)
    return md_block_lst

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDLIST = "unordered_list"
    ORDLIST = "ordered_list"

def block_to_block_type(block):
    #return blocktype based on md_block presented
    lines = block.split("\n")
    if block.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        return BlockType.HEAD
    if block.startswith("```") and block.endswith("```"):#list(filter(lambda x: x.startswith(("```")) and x.endswith(("```")), md_block)):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDLIST
    if all(line.startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDLIST
    #Default case, hence no need for else:
    return BlockType.PARA 
