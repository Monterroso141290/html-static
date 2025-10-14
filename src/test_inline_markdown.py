from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
from typing import List
import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, tn, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from extract_title import extract_title

class TestInlineMarkdown(unittest.TestCase):

    def test_no_delimiter_returns_unchanged(self):
        nodes = [tn("just text", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE)
        assert len(out) == 1 and out[0].text == "just text" and out[0].text_type == TextType.TEXT

    def test_non_text_nodes_passthrough(self):
        bold_node = tn("bold", TextType.BOLD)
        out = split_nodes_delimiter([bold_node], "`", TextType.CODE)
        assert out == [bold_node]

    def test_simple_code_split(self):
        nodes = [tn("Hello `code` world", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE)
        assert [ (n.text, n.text_type) for n in out ] == [
        ("Hello ", TextType.TEXT),
        ("code", TextType.CODE),
        (" world", TextType.TEXT),
    ]

    def test_single_link(self):
        node = TextNode(
            "Go to [Boot.dev](https://boot.dev)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Go to ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode(
            "Here is [one](url1) and [two](url2)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("one", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.LINK, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_no_link(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

def test_bold_split_with_double_asterisk():
    nodes = [tn("a **b** c", TextType.TEXT)]
    out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    assert [ (n.text, n.text_type) for n in out ] == [
        ("a ", TextType.TEXT),
        ("b", TextType.BOLD),
        (" c", TextType.TEXT),
    ]

def test_italic_split_with_underscore():
    nodes = [tn("x _y_ z", TextType.TEXT)]
    out = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    assert [ (n.text, n.text_type) for n in out ] == [
        ("x ", TextType.TEXT),
        ("y", TextType.ITALIC),
        (" z", TextType.TEXT),
    ]

def test_multiple_pairs_in_one_node():
    nodes = [tn("a `b` c `d` e", TextType.TEXT)]
    out = split_nodes_delimiter(nodes, "`", TextType.CODE)
    assert [ (n.text, n.text_type) for n in out ] == [
        ("a ", TextType.TEXT),
        ("b", TextType.CODE),
        (" c ", TextType.TEXT),
        ("d", TextType.CODE),
        (" e", TextType.TEXT),
    ]

def test_unmatched_raises():
    nodes = [tn("start `oops", TextType.TEXT)]
    with pytest.raises(ValueError):
        split_nodes_delimiter(nodes, "`", TextType.CODE)

def test_empty_parts_dropped_leading_and_trailing():
    nodes = [tn("`x`", TextType.TEXT)]
    out = split_nodes_delimiter(nodes, "`", TextType.CODE)
    # empty plain segments at both ends dropped
    assert [ (n.text, n.text_type) for n in out ] == [
        ("x", TextType.CODE),
    ]

def test_mixed_list_preserves_order():
    nodes = [
        tn("a `b`", TextType.TEXT),
        tn("C", TextType.BOLD),     # passthrough
        tn(" d `e` f", TextType.TEXT),
    ]
    out = split_nodes_delimiter(nodes, "`", TextType.CODE)
    assert [ (n.text, n.text_type) for n in out ] == [
        ("a ", TextType.TEXT),
        ("b", TextType.CODE),
        ("", TextType.TEXT)]  # depends on your empty handling; remove if you skip empties

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is a [link](https://example.com)"
    )
    self.assertListEqual([("link", "https://example.com")], matches)

def test_split_nodes_image(self):
    node = TextNode(
        "Here is an image: ![alt text](https://example.com/image.png) in the text.",
        TextType.TEXT,
    )
    result = split_nodes_image([node])
    expected = [
        TextNode("Here is an image: ", TextType.TEXT),
        TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
        TextNode(" in the text.", TextType.TEXT),
    ]
    assert result == expected

def test_split_nodes_image_no_image(self):
    node = TextNode("Just some text without an image.", TextType.TEXT)
    result = split_nodes_image([node])
    expected = [TextNode("Just some text without an image.", TextType.TEXT)]
    assert result == expected

class TestExtractTitle(unittest.TestCase):

    def test_basic_title(self):
        self.assertEqual(extract_title("# My Title"), "My Title")

    def test_title_with_leading_whitespace(self):
        self.assertEqual(extract_title("   # My Title"), "My Title")

    def test_no_title_raises(self):
        with self.assertRaises(Exception):
            extract_title("No title here")
