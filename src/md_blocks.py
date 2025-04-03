from enum import Enum

from textnode import *
from htmlnode import *
from splitdelimiter import *
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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown) #split markdown to blocks
    child_nodes = []
    html_parent = ParentNode("div", child_nodes)
    for block in blocks:
        block_type = block_to_block_type(block) #find the type of block
        if block_type == BlockType.PARA:
            block = block.replace("\n"," ")
            children = text_to_children(block)
            paragraph_node = ParentNode("p",children)
            child_nodes.append(paragraph_node)

        elif block_type == BlockType.HEAD:
            heading_node = process_heading(block)
            child_nodes.append(heading_node)
            
        elif block_type == BlockType.QUOTE:
            quote_items = []
            for line in block.split("\n"):
                if line.strip().startswith(">"):
                    quote_items.append(line.strip(">").strip())
            content = " ".join(quote_items)
            children = text_to_children(content)
            quote_node = ParentNode("blockquote", children)
            child_nodes.append(quote_node)

        elif block_type == BlockType.CODE:
            content = block[4:-3]
            code_node = TextNode(content, TextType.CODE)
            html_code_node = text_node_to_html_node(code_node)
            pre_code_node = ParentNode("pre", [html_code_node])
            child_nodes.append(pre_code_node)

        elif block_type == BlockType.UNORDLIST:
            ulist_items = []
            for line in block.split("\n"):
                if line.strip().startswith("-"):
                    content = line.strip()[1:].strip()
                    if content != "":
                        line_children = text_to_children(content)
                        list_node = ParentNode("li",line_children)
                        ulist_items.append(list_node)
            ul_node = ParentNode("ul", ulist_items)
            child_nodes.append(ul_node)

        elif block_type == BlockType.ORDLIST:
            olist_items = []
            for line in block.split("\n"):
                line = line.strip()
                if line != "" and "." in line:
                    period_index = line.index(".")
                    if line[:period_index].isdigit():
                        content = line[period_index + 1:].strip()
                        if content != "":
                            content_children = text_to_children(content)
                            list_node = ParentNode("li",content_children)
                            olist_items.append(list_node)
            ol_node = ParentNode("ol", olist_items)
            child_nodes.append(ol_node)

    return html_parent
        
        
def text_to_children(text):
    htmlnodes_lst = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        html_node = text_node_to_html_node(node)
        htmlnodes_lst.append(html_node)

    return htmlnodes_lst

def process_heading(text):
    stripped_text = text.lstrip("#")
    string_diff = len(text) - len(stripped_text)
    if 1 <= string_diff <= 6:

        if text[string_diff] == " ":
            content = text[string_diff + 1:]
            nodes = text_to_children(content)

            return ParentNode(f"h{string_diff}", nodes)
        else:
            raise Exception("Not a valid heading - no space after #")
    else:
        raise Exception("invalid number of #")
    
   
        #based on the type of block, create parent HTMLnode just a <div>
        #create a leafnode to HTMLnode
        #assign the children to the HTMLnode
        #text -> text_to_text_node -> text_node_to_html_node (returns leafnode)

    #1. Loop over blocks, for each block find the type of block
    #2. If block_type == "BlockType.PARA": HTMLnode(tag="p", value=None, children=None,props=None)
    #2a. Do if statements for each blocktype and create HTMLnode based on the blocktype
    #3. convert text to children htmlnode. Parse text using text_to_text_node(text), where text_to_text_node(text) parses inline markdown and turns into TextNode object. 
    #4. convert TextNodes to HTML using text_node_to_html_node based on textnode.type enum and returns Leafnodes with proper format based on blocktype.

    #create a new ParentNode(tag="div", child_nodes) at the top, and a new child_nodes list, 
    #and then append new ParentNodes(p,h1,blockquote,etc) into child_nodes, and ensure each ParentNodes(p,h1,blockquote) has appropriate LeafNodes.
    #For Code I would not parse text through text_to_textnodes and simply create a new TextNode obj holding the text.

    #A helper function, if BlockType.ORDEREDLIST: f"{entiretext}". Also split entiretext to replace "- " with "".(missing wrap at the end of each line) another function for BlockType.UNORDEREDLIST where instead of <ol> it will be<ul>.
    #Probably another create a helper function where I check for conditionals.
    #Split blocks, then if block.startswith("#"): ParentNode.tag = "H1" ?
    #a function where it applies text_to_textnodes to raw text, where multiple functions to parse inline markdown into textnodes has been created. Example:
   
