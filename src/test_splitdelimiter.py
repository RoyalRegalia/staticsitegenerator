import unittest

from textnode import *
from htmlnode import *
from splitdelimiter import *

class TestSplitDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is ", TextType.TEXT), 
                TextNode("bold", TextType.BOLD), 
                TextNode(" text", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_delimiter_italics_double_markdown(self):
        node = TextNode("This is _italic_ text _did you know?_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" text ", TextType.TEXT), TextNode("did you know?", TextType.ITALIC), TextNode("", TextType.TEXT)])

    def test_split_nodes_delimiter_code_bold(self):
        node = TextNode("This is `code block` text, **CODE** block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes2 = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes2, [TextNode("This is ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" text, ", TextType.TEXT), TextNode("CODE", TextType.BOLD), TextNode(" block", TextType.TEXT)])

    def test_split_nodes_delimiter_no_closing_markdown(self):
        node = TextNode("This is **bold text", TextType.TEXT)
        with self.assertRaises(ValueError) as e:
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(str(e.exception), "No matching delimiter '**' found")

    def test_split_nodes_no_delimiter(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is just plain text", TextType.TEXT)])

    def test_split_nodes_delimiter_empty_strings(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("", TextType.TEXT)])

if __name__ == "__main__":
    unittest.main()