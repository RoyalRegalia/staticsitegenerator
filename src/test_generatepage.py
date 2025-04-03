import unittest

from generatepage import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        text = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**."""
        tfc = extract_title(text)       
        self.assertEqual(tfc, "Tolkien Fan Club")

    def test_extract_title_two(self):
        text = "# Tolkien Fan Club"
        tfc = extract_title(text)       
        self.assertEqual(tfc, "Tolkien Fan Club")



    

if __name__ == "__main__":
    unittest.main()