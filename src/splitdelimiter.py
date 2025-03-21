from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    text_type = process_delimiter(delimiter)

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_nodes = node.text.split(delimiter)
            
            if len(split_nodes) % 2 == 0:
                raise ValueError(f"No matching delimiter '{delimiter}' found")

            for i in range(len(split_nodes)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_nodes[i], text_type))
                
        else:
            # For non-TextType.TEXT nodes, simply add them to new_nodes
            new_nodes.append(node)
    return new_nodes

def process_delimiter(delimiter): #used to process what delimiter it is
    delimiter_dict = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`":TextType.CODE
    }
    if delimiter == "": #if key is empty
        return TextType.TEXT #return value type text
    if delimiter in delimiter_dict: #if key in dict
        return delimiter_dict[delimiter] #return dict[key]'s value
    raise ValueError(f"Invalid delimiter: {delimiter}") #if outside of dict, raise error
