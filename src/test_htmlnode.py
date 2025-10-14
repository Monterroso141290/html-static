import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "This is a div", [], {"class": "container"})
        node2 = HTMLNode("div", "This is a div", [], {"class": "container"})
        self.assertEqual(node, node2)

    def test_eq_it(self):
        node = HTMLNode("span", "This is a span", [], {"class": "text"})
        node2 = HTMLNode("span", "This is a span", [], {"class": "text"})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("div", "This is a div", [], {"class": "container"})
        node2 = HTMLNode("div", "This is a different div", [], {"class": "container"})
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = HTMLNode("a", "Click here", [], {"href": "https://google.com"})
        node2 = HTMLNode("a", "Click here", [], {})
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()