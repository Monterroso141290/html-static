from markdown_blocks import markdown_to_html_node
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
import os
import sys
from extract_title import extract_title
from pathlib import Path


def generate_page(from_path, template_path, destination_path, basepath="/"):
    print(f"Generating page from {from_path} using template {template_path} to {destination_path}")

    # Read markdown and template
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title
    title = extract_title(markdown_content)

    # Replace placeholders
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # Apply basepath to all href/src that start with /
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    # Ensure directory exists
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    # Write HTML to destination
    with open(destination_path, "w", encoding="utf-8") as f:
        f.write(final_html)
