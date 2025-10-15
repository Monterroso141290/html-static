import os 
import shutil
import sys
from generate_pages_recursively import generate_pages_recursively
# hello world

from textnode import TextNode, TextType
from generate_page import generate_page
from generate_pages_recursively import generate_pages_recursively
from inline_markdown import text_to_textnodes



def recursive_copy(src, dst):
    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            os.makedirs(dst_path, exist_ok=True)
            recursive_copy(src_path, dst_path)

def main():
    # Basepath from CLI or default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    dst = 'docs'  # GitHub Pages directory
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)

    # Copy static files
    recursive_copy('static', dst)

    # Generate all markdown pages
    generate_pages_recursively("content", "template.html", dst, basepath)

if __name__ == "__main__":
    main()