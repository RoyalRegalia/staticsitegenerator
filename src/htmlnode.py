
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            print(f"LeafNode with tag '{self.tag}' has no value")
            raise ValueError("must have value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" #Parenthesis actually executes the function and gives the result, w/o parenthesis {self.props_to_html} prints the object
    
    def __repr__(self):
        #Always give yourself a method to print for debugging
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")

        child_htmls = ""
        for child in self.children:
            child_htmls += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_htmls}</{self.tag}>"
        
    def __repr__(self):
        return f"ParentNode({self.tag} children:{self.children}, {self.props})"
        

        