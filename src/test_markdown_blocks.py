from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
from typing import List
import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, tn, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, block_to_html_node

class TestMarkdownBlocks(unittest.TestCase):
    def test_single_paragraph(self):
        markdown = "This is a single paragraph."
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This is a single paragraph."])

    def test_multiple_paragraphs(self):
        markdown = "This is the first paragraph.\n\nThis is the second paragraph."
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This is the first paragraph.", "This is the second paragraph."])

    def test_leading_trailing_whitespace(self):
        markdown = "   This paragraph has leading and trailing whitespace.   "
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This paragraph has leading and trailing whitespace."])

    def test_empty_string(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [])

    def test_only_whitespace(self):
        markdown = "     \n   \n  "
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [])

    def test_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_type_code(self):
        block = "```\ncode block\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_type_quote(self):
        block = "> This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_type_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_type_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_type_paragraph(self):
        block = "Just a regular paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_heading_and_paragraph(self):
        md = "# Title\n\nHello **world**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>Title</h1>", html)
        self.assertIn("<p>Hello <b>world</b></p>", html)

    def test_list(self):
        md = "- One\n- Two"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<ul>", html)
        self.assertIn("<li>One</li>", html)
        self.assertIn("<li>Two</li>", html)