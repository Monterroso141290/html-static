import os
from markdown_blocks import markdown_to_html_node

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath="/"):
    os.makedirs(dest_dir_path, exist_ok=True)

    # Load template once
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    for item in os.listdir(dir_path_content):
        full_entry_path = os.path.join(dir_path_content, item)
        dest_entry_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(full_entry_path):
            generate_pages_recursively(full_entry_path, template_path, dest_entry_path, basepath)

        elif item.endswith(".md"):
            with open(full_entry_path, "r", encoding="utf-8") as md_file:
                markdown = md_file.read()

            html_node = markdown_to_html_node(markdown)
            html_content = html_node.to_html()

            # Combine with template
            full_html = template.replace("{{ Content }}", html_content)

            # Replace root-relative paths with basepath
            full_html = full_html.replace('href="/', f'href="{basepath}')
            full_html = full_html.replace('src="/', f'src="{basepath}')

            dest_file_path = os.path.splitext(dest_entry_path)[0] + ".html"
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)

            with open(dest_file_path, "w", encoding="utf-8") as out_file:
                out_file.write(full_html)

            print(f"Generated {dest_file_path} from {full_entry_path}")
