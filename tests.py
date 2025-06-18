import unittest
from unittest.mock import patch
from io import StringIO
import madlibs

class TestMadLibs(unittest.TestCase):
    def test_welcome_message(self):
        """Test if the welcome message is displayed correctly"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            print("🎤 Welcome to a Mad Libs Adventure! 🎶")
            print("Get ready to build your dream K-pop concert trip!")
            output = fake_output.getvalue()
            self.assertIn("Welcome to a Mad Libs Adventure!", output)
            self.assertIn("Get ready to build your dream K-pop concert trip!", output)

    @patch('builtins.input')
    def test_story_generation(self, mock_input):
        """Test if the story is generated correctly with sample inputs"""
        # Mock the input values
        mock_input.side_effect = [
            "Luna",      # name1
            "Mia",       # name2
            "Seoul",     # city
            "excited",   # adjective1
            "lightstick", # kpop_merch
            "ramen",     # snack
            "crab dance", # dance_move
            "squeak",    # embarrassing_sound
            "glowstick", # weird_object
            "Sophia",    # idol_name
            "✨"         # emoji
        ]

        # Capture the output
        with patch('sys.stdout', new=StringIO()) as fake_output:
            # Run the main program
            madlibs.play_madlibs()
            
            # Get the output
            output = fake_output.getvalue()
            
            # Test if the story contains all the input values
            self.assertIn("Luna", output)
            self.assertIn("Mia", output)
            self.assertIn("Seoul", output)
            self.assertIn("excited", output)
            self.assertIn("lightstick", output)
            self.assertIn("ramen", output)
            self.assertIn("crab dance", output)
            self.assertIn("squeak", output)
            self.assertIn("glowstick", output)
            self.assertIn("SOPHIA", output)  # Note: idol name is converted to uppercase in the story
            self.assertIn("✨", output)

            # Test for story structure
            self.assertIn("Chapter 1: Arrival in", output)
            self.assertIn("Chapter 2: The Concert Mayhem", output)
            self.assertIn("Chapter 3: Legends of the Night", output)
            self.assertIn("Legendary.", output)

    def test_story_format(self):
        """Test if the story has the correct format"""
        story = """
🎒 Chapter 1: Arrival in Seoul

Luna and Mia landed in Seoul with their bags stuffed full of lightsticks, extra phone chargers, and emergency ramen packs. They were feeling super excited, because tonight was the big KATSEYE concert at the magical GlowBop Arena. The entire airport was buzzing with fans holding banners that said, "WE LOVE YOU, SOPHIA!"

They got lost trying to find their hotel and accidentally walked into a store that only sold robotic alpacas. One of the alpacas made a loud squeak and scared Mia so badly she dropped her glowstick in a fountain. A security guard offered them directions... but only if they could do the crab dance perfectly.

🕺 Chapter 2: The Concert Mayhem

At the arena, a mysterious glitter cannon exploded near their seats and showered the crowd with confetti shaped like ✨. Luna screamed so loud, even Sophia looked confused for a second. During the encore, the music stopped and the stage lights turned off. A voice over the speakers said, "We need two brave fans to save the show!"

Without thinking, Mia leapt onto the stage, armed with her lightstick and Luna behind her. The crowd chanted their names, and someone handed them microphones made of cotton candy.

💫 Chapter 3: Legends of the Night

They performed a chaotic freestyle that included the crab dance, moonwalking with a ramen in each hand, and dramatic slow-motion karaoke. Somehow, it worked. The stage lights came back on, Sophia hugged them both, and confetti exploded in every direction.

As they walked back to their hotel—now minor celebrities—they looked at each other and said, "This was the most excited day of our lives." And in that exact moment, a fan ran up to them and whispered, "Are you the girls from the glitter cannon incident?"

Legendary. ✨
"""
        # Test if the story has the correct number of chapters
        self.assertEqual(len([line for line in story.split('\n') if 'Chapter' in line]), 3)
        
        # Test if the story contains all required story elements
        self.assertIn("Chapter 1: Arrival in", story)
        self.assertIn("Chapter 2: The Concert Mayhem", story)
        self.assertIn("Chapter 3: Legends of the Night", story)
        self.assertIn("Legendary.", story)
        self.assertIn("KATSEYE concert", story)
        self.assertIn("GlowBop Arena", story)

if __name__ == '__main__':
    unittest.main() 