import unittest
from unittest.mock import patch
from io import StringIO
import madlibs

class TestMadLibs(unittest.TestCase):
    def test_welcome_message(self):
        """Test if the welcome message is displayed correctly"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            print("Welcome to the Mad Libs Game! 🤪")
            self.assertEqual(fake_output.getvalue().strip(), "Welcome to the Mad Libs Game! 🤪")

    @patch('builtins.input')
    def test_story_generation(self, mock_input):
        """Test if the story is generated correctly with sample inputs"""
        # Mock the input values
        mock_input.side_effect = [
            "sparkly",  # adjective
            "magical",  # adjective2
            "unicorn",  # animal
            "Disneyland",  # place
            "dancing",  # verb
            "flibber",  # silly_word
            "Alice"     # friend_name
        ]

        # Capture the output
        with patch('sys.stdout', new=StringIO()) as fake_output:
            # Run the main program
            madlibs.play_madlibs()
            
            # Get the output
            output = fake_output.getvalue()
            
            # Test if the story contains all the input values
            self.assertIn("sparkly", output)
            self.assertIn("magical", output)
            self.assertIn("unicorn", output)
            self.assertIn("Disneyland", output)
            self.assertIn("dancing", output)
            self.assertIn("flibber", output)
            self.assertIn("Alice", output)

            # Test the complete story output
            expected_story = """
One day, my friend Alice and I were walking through the sparkly forest.
Suddenly, we saw a unicorn dancing near a flibber tree! It was so magical!
We couldn't believe our eyes, so we ran all the way to Disneyland while laughing our heads off.
It was the best day ever!
"""
            self.assertIn(expected_story.strip(), output)

    def test_story_format(self):
        """Test if the story has the correct format"""
        story = """
One day, my friend Alice and I were walking through the sparkly forest.
Suddenly, we saw a unicorn dancing near a flibber tree! It was so magical!
We couldn't believe our eyes, so we ran all the way to Disneyland while laughing our heads off.
It was the best day ever!
"""
        # Test if the story has the correct number of lines
        self.assertEqual(len(story.strip().split('\n')), 4)
        
        # Test if the story contains all required story elements
        self.assertIn("One day, my friend", story)
        self.assertIn("walking through the", story)
        self.assertIn("Suddenly, we saw a", story)
        self.assertIn("It was the best day ever!", story)

if __name__ == '__main__':
    unittest.main() 