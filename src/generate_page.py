from markdown_blocks import markdown_to_html_node
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
import os
import sys
from extract_title import extract_title
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, destination_path):
    print(f"Generating page from {from_path} using template {template_path} to {destination_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    
    #we convert the markdown to an html node first
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    #we use the extract_title to find the H1 header of the markdown file
    title = extract_title(markdown_content)

    # We replace the placeholders in the template with actual content
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)


    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    with open(destination_path, "w", encoding="utf-8") as f:
        f.write(final_html)