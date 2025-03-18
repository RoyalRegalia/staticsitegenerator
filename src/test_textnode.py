import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a normal node", TextType.NORMAL)
        node4 = TextNode("Can I URL?", TextType.LINK, "https://www.boot.dev")
        node5 = TextNode("noURL", TextType.NORMAL,"")
        node6 = TextNode("noURL", TextType.NORMAL,"www.boot.dev")
        self.assertEqual(node, node2)
        
        self.assertNotEqual(node5, node6)
    def test_not_eq(self):
        node = TextNode("This is a normal node", TextType.BOLD)
        node2 = TextNode("This is a normal node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode("noURL", TextType.LINK, None)
        node2 = TextNode("noURL", TextType.LINK)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()