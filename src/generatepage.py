import os

from md_blocks import *

def extract_title(markdown):
    split_text = markdown.split("\n")
    if split_text[0].startswith("# "):
        return split_text[0].strip("#").strip()
    raise Exception("Heading 1 not found. Make sure H1 formatting is correct")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md:
        md_file = md.read()
    
    with open(template_path) as temp:
        template_file = temp.read()
    
    convert = markdown_to_html_node(md_file)
    content_html = convert.to_html()

    title = extract_title(md_file)
    new_file = template_file.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as nw:
        nw.write(new_file)

def generate_pages_recursive(content_path, template_path, destination_path):
    #os.listdir the directories in content path
        #for each item in os.listdir
        #