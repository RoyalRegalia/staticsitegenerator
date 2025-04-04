import os
import shutil

from copystatic import copy_directory
from generatepage import generate_pages_recursive

source_dir = './static'
destination_dir = './public'
content_dir = "./content"
template_path = "./template.html"

def main():
    if not os.path.exists(source_dir):
        print(f"Error: The source directory '{source_dir}' does not exist.")
        return

    print("Checking for public directory...")
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
        print("Deleted existingpublic directory.")
    print(f"Copying files from {source_dir} to {destination_dir}")
    copy_directory(source_dir, destination_dir)

    print("Generating content...")
    generate_pages_recursive(content_dir, template_path, destination_dir)

main()