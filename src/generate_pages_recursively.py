import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    # this function recursively generates HTML pages from markdown files in dir_path_content.
    # keeps folder structure in dest_dir_path.
    # uses template_path as the HTML template.

    #we first ensure that the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)

    # We load the template content once
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # we go through every file/folder in the content directory
    for item in os.listdir(dir_path_content):
        full_entry_path = os.path.join(dir_path_content, item)
        dest_entry_path = os.path.join(dest_dir_path, item)

        # if its a directory, we call this function recursively
        if os.path.isdir(full_entry_path):
            generate_pages_recursively(full_entry_path, template_path, dest_entry_path)

        #else, it its a markdown file
        elif item.endswith(".md"):
            # we read the markdown content
            with open(full_entry_path, "r", encoding="utf-8") as md_file:
                markdown = md_file.read()

            #we convert the markdown to an html node first
            html_node = markdown_to_html_node(markdown)
            html_content = html_node.to_html()

            #Combine with template
            full_html = template.replace("{{ Content }}", html_content)

            os.makedirs(os.path.dirname(dest_entry_path), exist_ok=True)
            #we write the corresponding .html file in the destination directory
            dest_file_path = os.path.splitext(dest_entry_path)[0] + ".html"


            with open(dest_file_path, "w", encoding="utf-8") as out_file:
                out_file.write(full_html)

                print(f"Generated {dest_file_path} from {full_entry_path}")