from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
from typing import List

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not delimiter:
        raise ValueError("Delimiter cannot be empty")

    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        parts = node.text.split(delimiter)
        if (len(parts) - 1) % 2 != 0:
            raise ValueError("Invalid Markdown: unmatched delimiter")

        for i, part in enumerate(parts):
            ttype = text_type if i % 2 == 1 else TextType.TEXT
            if part:
                result.append(TextNode(part, ttype))
    return result

def split_nodes_image(old_nodes):
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        if not images:
            final_list.append(node)
            continue

        for alt_text, url in images:
            parts = text.split(f"![{alt_text}]({url})",1)
            before = parts[0]
            after = parts[1] if len(parts) > 1 else ""

            if before:
                final_list.append(TextNode(before, TextType.TEXT))
            final_list.append(TextNode(alt_text, TextType.IMAGE, url=url))
            text =  after

        if text:
            final_list.append(TextNode(text, TextType.TEXT))

    return final_list

def split_nodes_link(old_nodes):
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(text)

        if not links:
            final_list.append(node)
            continue
        
        for link_text, url in links:
            parts = text.split(f"[{link_text}]({url})", 1)
            before = parts[0]
            after = parts[1] if len(parts) > 1 else ""

            if before:
                final_list.append(TextNode(before, TextType.TEXT))
            final_list.append(TextNode(link_text, TextType.LINK, url=url))
            text = after

        if text:
            final_list.append(TextNode(text, TextType.TEXT))

    return final_list

def tn(text, t):  # helper
    return TextNode(text, t)



def extract_markdown_images(text):
    import re
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return [ (m[0], m[1]) for m in matches ]
    # returns list of (alt_text, url) tuples

def extract_markdown_links(text):
    import re
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return [ (m[0], m[1]) for m in matches ]
    # returns list of (link_text, url) tuples

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    dbg("after code", nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    dbg("after bold", nodes)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    dbg("after star", nodes)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    dbg("after underscore", nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def dbg(tag, nodes):
    print(tag, [(n.text, n.text_type) for n in nodes])

if __name__ == "__main__":
    text_to_textnodes("Disney _didn't ruin it_ (okay, but Amazon might have)")