from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from typing import List
from enum import Enum
from inline_markdown import split_nodes_delimiter, tn, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str):
    lines = block.splitlines()
    stripped_block = block.strip()
    
    if stripped_block.startswith("#"):
        return BlockType.HEADING
    elif stripped_block.startswith("```") and stripped_block.endswith("```"):
        return BlockType.CODE
    elif stripped_block.startswith(">"):
        return BlockType.QUOTE

    # check unordered list
    for line in lines:
        if line.strip().startswith("- "):
            return BlockType.UNORDERED_LIST

    # check ordered list
    expected_number = 1
    for line in lines:
        line = line.strip()
        if line.startswith(f"{expected_number}. "):
            expected_number += 1
        else:
            break
    if expected_number >= 2:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str):
    markdown = markdown.strip()
    blocks = markdown.split("\n\n")
    final_list = []
    for block in blocks:
        block = block.strip()
        if block:
            final_list.append(block)
    return final_list

def markdown_to_html_node(markdown: str):
    

    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            children.append(block_to_html_node(block, block_type))
        elif block_type == BlockType.PARAGRAPH:
            children.append(block_to_html_node(block, block_type))
        elif block_type == BlockType.QUOTE:
            children.append(block_to_html_node(block, block_type))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(block_to_html_node(block, block_type))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(block_to_html_node(block, block_type))
        elif block_type == BlockType.CODE:
            children.append(block_to_html_node(block, block_type))
        else:
            raise Exception(f"Unknown block type: {block_type}")

    # Wrap all block nodes in a parent <div>
    return ParentNode("div", children)

def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def block_to_html_node(block: str, block_type: BlockType):
    if block_type == BlockType.PARAGRAPH:
        textnodes = text_to_textnodes(block)
        children = [text_node_to_html_node(tn) for tn in textnodes]
        return ParentNode("p", children)
    elif block_type == BlockType.HEADING:
        level = len(block) - len(block.lstrip('#'))
        text = block[level:].strip()
        textnodes = text_to_textnodes(text)
        children = [text_node_to_html_node(tn) for tn in textnodes]
        return ParentNode(f"h{level}", children)
    elif block_type == BlockType.CODE:
        code_content = "\n".join(block.splitlines()[1:-1])
        textnode = TextNode(code_content, TextType.TEXT)
        html_node = text_node_to_html_node(textnode)
        return ParentNode("pre", [ParentNode("code", [html_node])])

    elif block_type == BlockType.QUOTE:
        lines = block.splitlines()
        cleaned_lines = [line.lstrip('>').strip() for line in lines]
        text = "\n".join(cleaned_lines)
        textnodes = text_to_textnodes(text)
        children = [text_node_to_html_node(node) for node in textnodes]
        return ParentNode("blockquote", children)
    elif block_type == BlockType.UNORDERED_LIST:
        items = [line[2:].strip() for line in block.splitlines() if line.strip().startswith("- ")]
        li_nodes = []
        for item in items:
            print("UL item ->", repr(item))  # TEMP DEBUG
            textnodes = text_to_textnodes(item)
            children = [text_node_to_html_node(tn) for tn in textnodes]
            li_nodes.append(ParentNode("li", children))
        return ParentNode("ul", li_nodes)
    elif block_type == BlockType.ORDERED_LIST:
        items = [
            line.strip().split(". ", 1)[1].strip()
            for line in block.splitlines()
            if ". " in line.strip()
]
        li_nodes = []
        for item in items:
            textnodes = text_to_textnodes(item)
            children = [text_node_to_html_node(tn) for tn in textnodes]
            li_nodes.append(ParentNode("li", children))
        return ParentNode("ol", li_nodes)
    else:
        raise Exception("Unsupported block type.")