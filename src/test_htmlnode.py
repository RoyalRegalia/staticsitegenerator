import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"href": "https://www.google.com"}
        node = HTMLNode("a", "mamamia", None, props)
        
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
        
    def test_value(self):
        node = HTMLNode("a", "This is hard")
        self.assertEqual(node.value, "This is hard")
    
    def test_tag(self):
        node = HTMLNode("H1", "Header")
        self.assertNotEqual(node.tag, "h1")
    
    def test_repr(self):
        node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), '<b>Hello, world!</b>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_child_error(self):
        parent_node = ParentNode("p",None)
        #Test that ValueError is raised when to_html is called
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_tag_error(self):
        child_node = LeafNode("b","omega")
        parent_node = ParentNode(None,[child_node])
        #Test that ValueError is raised with the correct message
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()

        self.assertEqual(str(e.exception), "ParentNode must have tag")
    
    def test_to_html_multiple_parent_with_one_parent_tag(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode(None, [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()