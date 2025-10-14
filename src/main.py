import os 
import shutil
# hello world

from textnode import TextNode, TextType
from generate_page import generate_page
from generate_pages_recursively import generate_pages_recursively
from inline_markdown import text_to_textnodes



def recursive_copy(src, dst):
    #Listdir() lists everything in order - Files and subdirectories
    for name in os.listdir(src):
        #This builds the full path for both src and dst
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)

        #We check is the item is a directory or file
        if os.path.isfile(src_path):
            print (f"Copying file: {src_path} to {dst_path}")
            #shutil copies contents and permissions
            shutil.copy(src_path, dst_path)
        else:
            print (f"Entering directory: {src_path}")
            os.mkdir(dst_path)
            #we call our function  recursively for the subfolder
            recursive_copy(src_path, dst_path)

def main():
    # Create a TextNode with dummy values
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

    src = 'static'
    dst = 'public'

    if os.path.exists(dst):
        print(f"Deleting existing '{dst}' directory...")
        shutil.rmtree(dst)
        # Ensure the directory is fully deleted before proceeding
        # We delete this to make sure we're not copying over old files
    

    print(f"Copying '{src}' to '{dst}'...")
    os.mkdir(dst)
    # We create the directory first to avoid issues on some systems.

    #We call our function once and it will take care of the rest if it needs recursion
    recursive_copy(src, dst)

    generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursively("content", "template.html", "public")

#When we run python3 src/main.py this will be the entry point        
if __name__ == "__main__":
    text_to_textnodes("Disney _didn't ruin it_ (okay, but Amazon might have)")
    main()