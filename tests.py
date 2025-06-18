import unittest
from unittest.mock import patch
from io import StringIO
import madlibs

class TestMadLibs(unittest.TestCase):
    def test_welcome_message(self):
        """Test if the welcome message is displayed correctly"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            madlibs.print("Welcome to the Mad Libs Game! 🤪")
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
            # Run the main program logic
            adjective = input("Enter an adjective: ")
            adjective2 = input("Enter an adjective: ")
            animal = input("Enter an animal: ")
            place = input("Enter a place: ")
            verb = input("Enter a verb ending in -ing: ")
            silly_word = input("Enter a silly made-up word: ")
            friend_name = input("Enter your friend's name: ")

            story = f"""
One day, my friend {friend_name} and I were walking through the {adjective} forest.
Suddenly, we saw a {animal} {verb} near a {silly_word} tree! It was so {adjective2}!
We couldn't believe our eyes, so we ran all the way to {place} while laughing our heads off.
It was the best day ever!
"""

            # Test if the story contains all the input values
            self.assertIn("sparkly", story)
            self.assertIn("magical", story)
            self.assertIn("unicorn", story)
            self.assertIn("Disneyland", story)
            self.assertIn("dancing", story)
            self.assertIn("flibber", story)
            self.assertIn("Alice", story)

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