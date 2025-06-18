import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import font as tkfont

class KATLibsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 K-pop Concert KATLibs 🎶")
        self.root.geometry("800x600")
        
        # Pink color palette
        self.colors = {
            'bg': '#FFF0F5',  # Lavender blush
            'title': '#FF1493',  # Deep pink
            'subtitle': '#FF69B4',  # Hot pink
            'button': '#FF69B4',  # Hot pink
            'button_text': '#FFFFFF',  # White
            'label': '#DB7093',  # Pale violet red
            'entry_bg': '#FFB6C1',  # Light pink
            'entry_fg': '#4B0082',  # Indigo
            'story_bg': '#FFE4E1',  # Misty rose
            'story_fg': '#8B008B'  # Dark magenta
        }
        
        self.root.configure(bg=self.colors['bg'])

        # Set up custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.story_font = tkfont.Font(family="Helvetica", size=12)

        # Create main frame with pink background
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title with sparkle effect
        self.title_label = tk.Label(
            self.main_frame,
            text="✨ K-pop Concert KATLibs ✨",
            font=self.title_font,
            bg=self.colors['bg'],
            fg=self.colors['title']
        )
        self.title_label.pack(pady=20)

        # Subtitle with more sparkles
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="🌟 Create your dream K-pop concert adventure! 🌟",
            font=self.label_font,
            bg=self.colors['bg'],
            fg=self.colors['subtitle']
        )
        self.subtitle_label.pack(pady=10)

        # Input frame with pink background
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=20)

        # Create input fields
        self.entries = {}
        self.create_input_field("name1", "Your name:")
        self.create_input_field("name2", "Your sister/friend's name:")
        self.create_input_field("city", "Choose a city (Seoul or Tokyo):")
        self.create_input_field("adjective1", "An adjective to describe your mood:")
        self.create_input_field("kpop_merch", "A piece of K-pop merch (e.g., lightstick, hoodie):")
        self.create_input_field("snack", "A snack:")
        self.create_input_field("dance_move", "A silly dance move:")
        self.create_input_field("embarrassing_sound", "An embarrassing sound (e.g., burp, squeak):")
        self.create_input_field("weird_object", "A weird object you could carry:")
        self.create_input_field("idol_name", "A KATSEYE member's name:")
        self.create_input_field("emoji", "Your favorite emoji:")

        # Create story button with sparkle effect
        self.create_button = tk.Button(
            self.main_frame,
            text="✨ Create My Story! ✨",
            command=self.create_story,
            font=self.button_font,
            bg=self.colors['button'],
            fg=self.colors['button_text'],
            relief=tk.RAISED,
            padx=20,
            pady=10,
            cursor="heart"  # Heart cursor on hover
        )
        self.create_button.pack(pady=20)

        # Story display with pink theme
        self.story_text = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            width=60,
            height=10,
            font=self.story_font,
            bg=self.colors['story_bg'],
            fg=self.colors['story_fg']
        )
        self.story_text.pack(pady=20, fill=tk.BOTH, expand=True)

    def create_input_field(self, field_name, label_text):
        frame = ttk.Frame(self.input_frame)
        frame.pack(fill=tk.X, pady=5)
        
        label = tk.Label(
            frame,
            text=label_text,
            font=self.label_font,
            bg=self.colors['bg'],
            fg=self.colors['label'],
            width=30,
            anchor="e"
        )
        label.pack(side=tk.LEFT, padx=5)
        
        entry = tk.Entry(
            frame,
            font=self.label_font,
            width=30,
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg'],
            insertbackground=self.colors['entry_fg']  # Cursor color
        )
        entry.pack(side=tk.LEFT, padx=5)
        
        self.entries[field_name] = entry

    def create_story(self):
        # Get all input values
        inputs = {field: entry.get() for field, entry in self.entries.items()}
        
        # Create the story using the madlibs module
        story = f"""
🎒 Chapter 1: Arrival in {inputs['city']}

{inputs['name1']} and {inputs['name2']} landed in {inputs['city']} with their bags stuffed full of {inputs['kpop_merch']}s, extra phone chargers, and emergency {inputs['snack']} packs. They were feeling super {inputs['adjective1']}, because tonight was the big KATSEYE concert at the magical GlowBop Arena. The entire airport was buzzing with fans holding banners that said, "WE LOVE YOU, {inputs['idol_name'].upper()}!"

They got lost trying to find their hotel and accidentally walked into a store that only sold robotic alpacas. One of the alpacas made a loud {inputs['embarrassing_sound']} and scared {inputs['name2']} so badly she dropped her {inputs['weird_object']} in a fountain. A security guard offered them directions... but only if they could do the {inputs['dance_move']} perfectly.

🕺 Chapter 2: The Concert Mayhem

At the arena, a mysterious glitter cannon exploded near their seats and showered the crowd with confetti shaped like {inputs['emoji']}. {inputs['name1']} screamed so loud, even {inputs['idol_name']} looked confused for a second. During the encore, the music stopped and the stage lights turned off. A voice over the speakers said, "We need two brave fans to save the show!"

Without thinking, {inputs['name2']} leapt onto the stage, armed with her {inputs['kpop_merch']} and {inputs['name1']} behind her. The crowd chanted their names, and someone handed them microphones made of cotton candy.

💫 Chapter 3: Legends of the Night

They performed a chaotic freestyle that included the {inputs['dance_move']}, moonwalking with a {inputs['snack']} in each hand, and dramatic slow-motion karaoke. Somehow, it worked. The stage lights came back on, {inputs['idol_name']} hugged them both, and confetti exploded in every direction.

As they walked back to their hotel—now minor celebrities—they looked at each other and said, "This was the most {inputs['adjective1']} day of our lives." And in that exact moment, a fan ran up to them and whispered, "Are you the girls from the glitter cannon incident?"

Legendary. {inputs['emoji']}
"""
        # Display the story
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(tk.END, story)

def main():
    root = tk.Tk()
    KATLibsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()  