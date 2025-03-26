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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([('image', 'https://i.imgur.com/zjjcJKZ.png')], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.youtube.com)"
        )
        self.assertListEqual([('link', 'https://www.youtube.com')], matches)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
             new_nodes,
        )

    def test_split_nodes_image_no_img(self):
        node = TextNode("No Image",TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("No Image", TextType.TEXT)], new_nodes)

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT), 
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
                TextNode(" and ", TextType.TEXT), 
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")

            ],
            new_nodes
        )

    def test_split_nodes_link_and_image(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes2 = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT), 
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
                TextNode(" and ", TextType.TEXT), 
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes2
        )
    
    def test_split_nodes_image_two(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT), 
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), 
                TextNode(" and another ", TextType.TEXT), 
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")

            ],
            new_nodes
        )
    
    def test_text_to_textnodes(self):
        test = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            test
        )
        
if __name__ == "__main__":
    unittest.main()