import re

from textnode import *
from htmlnode import *

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    bold_split_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
    italic_split_nodes = split_nodes_delimiter(bold_split_nodes, '_', TextType.ITALIC)
    code_split_nodes = split_nodes_delimiter(italic_split_nodes, '`', TextType.CODE)
    link_split_nodes = split_nodes_link(code_split_nodes)
    image_split_nodes = split_nodes_image(link_split_nodes)
    final_split_nodes = image_split_nodes

    return final_split_nodes
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    text_type = process_delimiter(delimiter) #find text_type variable with helper function

    for node in old_nodes: #for every TextNode in old_nodes
        if node.text_type == TextType.TEXT: #If the node text_type is TEXT,
            split_nodes = node.text.split(delimiter) #store new variable collecting text split based on delimiter
            
            if len(split_nodes) % 2 == 0: #if the total index count (len) in split_nodes is divisible by 2 hence even, 
                raise ValueError(f"No matching delimiter '{delimiter}' found") #a closing markdown pair is missing

            for i in range(len(split_nodes)): #for each data entry index count (len) in split_nodes,
                if i % 2 == 0: #if divisible by 2 hence even,
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

def extract_markdown_images(text):
    alt_url = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_url

def extract_markdown_links(text):
    alt_url = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_url

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            extracted_img = extract_markdown_images(node.text)
        
            if extracted_img:
                img_alt, img_link = extracted_img[0]
                parts = node.text.split(f"![{img_alt}]({img_link})", 1)

                if parts[0] != "":
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
                new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_link))

                if parts[1] != "":  
                    remaining_text_node = TextNode(parts[1], TextType.TEXT)
                    remaining_nodes = split_nodes_image([remaining_text_node])
                    new_nodes.extend(remaining_nodes)

            else:
                new_nodes.append(node)
        else:
            # For non-TextType.TEXT nodes, simply add them to new_nodes
            new_nodes.append(node)
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            extracted_link = extract_markdown_links(node.text)
        
            if extracted_link:
                link_alt, link_url = extracted_link[0]
                parts = node.text.split(f"[{link_alt}]({link_url})", 1)

                if parts[0] != "":
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
                new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))

                if parts[1] != "":  
                    remaining_text_node = TextNode(parts[1], TextType.TEXT)
                    remaining_nodes = split_nodes_link([remaining_text_node])
                    new_nodes.extend(remaining_nodes)

            else:
                new_nodes.append(node)
        else:
            # For non-TextType.TEXT nodes, simply add them to new_nodes
            new_nodes.append(node)
            
    return new_nodes
    
def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    bold_split_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
    italic_split_nodes = split_nodes_delimiter(bold_split_nodes, '_', TextType.ITALIC)
    code_split_nodes = split_nodes_delimiter(italic_split_nodes, '`', TextType.CODE)
    link_split_nodes = split_nodes_link(code_split_nodes)
    image_split_nodes = split_nodes_image(link_split_nodes)
    final_split_nodes = image_split_nodes

    return final_split_nodes
