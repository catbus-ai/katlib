import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import font as tkfont

class KATLibsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 K-pop Concert KATLibs 🎶")
        self.root.geometry("900x600")
        
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
            'story_fg': '#FF1493'  
        }
        
        self.root.configure(bg=self.colors['bg'])

        # Set up custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.story_font = tkfont.Font(family="Helvetica", size=12)

        # Create main frame with pink background
        self.main_frame = tk.Frame(root, bg=self.colors['bg'], padx=20, pady=20)
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
        self.input_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        self.input_frame.pack(pady=20)

        # Create input fields
        self.entries = {}
        self.input_fields = [
            ("name1", "Your name:"),
            ("name2", "Your sister/friend's name:"),
            ("city", "Choose a city (Seoul or Tokyo):"),
            ("adjective1", "An adjective to describe your mood:"),
            ("kpop_merch", "A piece of K-pop merch (e.g., lightstick, hoodie):"),
            ("snack", "A snack:"),
            ("dance_move", "A silly dance move:"),
            ("embarrassing_sound", "An embarrassing sound (e.g., burp, squeak):"),
            ("weird_object", "A weird object you could carry:"),
            ("idol_name", "A KATSEYE member's name:"),
            ("emoji", "Your favorite emoji:")
        ]
        for idx, (field, label) in enumerate(self.input_fields):
            self.create_input_field(field, label, idx)

        # Create story button, vertically centered next to input fields
        self.create_button = tk.Button(
            self.input_frame,
            text="✨ Create My Story! ✨",
            command=self.create_story,
            font=self.button_font,
            bg=self.colors['button'],
            fg="#000000",
            relief=tk.RAISED,
            padx=20,
            pady=10,
            cursor="heart"
        )
        self.create_button.grid(row=0, column=2, rowspan=len(self.input_fields), padx=(30,0), pady=5, sticky="nsw")

    def create_input_field(self, field_name, label_text, row):
        label = tk.Label(
            self.input_frame,
            text=label_text,
            font=self.label_font,
            bg=self.colors['bg'],
            fg=self.colors['label'],
            wraplength=250,
            justify="right",
            anchor="e"
        )
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(
            self.input_frame,
            font=self.label_font,
            width=30,
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg'],
            insertbackground=self.colors['entry_fg']
        )
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
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
        # Open a new window for the story
        story_win = tk.Toplevel(self.root)
        story_win.title("Your K-pop Katlib Story!")
        story_win.configure(bg=self.colors['bg'])
        text_widget = tk.Text(
            story_win,
            wrap=tk.WORD,
            font=self.story_font,
            bg="#FFFFFF",
            fg="#000000",
            width=80,
            height=25
        )
        text_widget.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        # Insert story and highlight user words
        start = 0
        for key, value in inputs.items():
            if value:
                # Replace all occurrences with a unique marker
                story = story.replace(value, f"[[[{key}]]]")
        # Insert story and tag user words
        idx = 0
        while idx < len(story):
            if story[idx:idx+3] == "[[[":
                end_idx = story.find("]]]", idx)
                if end_idx != -1:
                    key = story[idx+3:end_idx]
                    value = inputs.get(key, "")
                    if value:
                        text_widget.insert(tk.END, value, ("userword",))
                    idx = end_idx + 3
                else:
                    text_widget.insert(tk.END, story[idx], ())
                    idx += 1
            else:
                text_widget.insert(tk.END, story[idx], ())
                idx += 1
        text_widget.tag_configure("userword", foreground="#C800A1", font=("Helvetica", 12, "bold"))
        text_widget.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    KATLibsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()  