def play_madlibs():
    print("🎤 Welcome to a Mad Libs Adventure! 🎶")
    print("Get ready to build your dream K-pop concert trip!")

    # Ask the player for some words
    name1 = input("Enter your name: ")
    name2 = input("Enter your sister/friend's name: ")
    city = input("Choose a city (Seoul or Tokyo): ")
    adjective1 = input("Enter an adjective to describe your mood: ")
    kpop_merch = input("Enter a piece of K-pop merch (e.g., lightstick, hoodie): ")
    snack = input("Enter a snack: ")
    dance_move = input("Enter a silly dance move: ")
    embarrassing_sound = input("Enter an embarrassing sound (e.g., burp, squeak): ")
    weird_object = input("Enter a weird object you could carry: ")
    idol_name = input("Enter a KATSEYE member’s name: ")
    emoji = input("Enter your favorite emoji: ")

    # Create the story
    story = f"""
🎒 Chapter 1: Arrival in {city}

{name1} and {name2} landed in {city} with their bags stuffed full of {kpop_merch}s, extra phone chargers, and emergency {snack} packs. They were feeling super {adjective1}, because tonight was the big KATSEYE concert at the magical GlowBop Arena. The entire airport was buzzing with fans holding banners that said, "WE LOVE YOU, {idol_name.upper()}!"

They got lost trying to find their hotel and accidentally walked into a store that only sold robotic alpacas. One of the alpacas made a loud {embarrassing_sound} and scared {name2} so badly she dropped her {weird_object} in a fountain. A security guard offered them directions... but only if they could do the {dance_move} perfectly.

🕺 Chapter 2: The Concert Mayhem

At the arena, a mysterious glitter cannon exploded near their seats and showered the crowd with confetti shaped like {emoji}. {name1} screamed so loud, even {idol_name} looked confused for a second. During the encore, the music stopped and the stage lights turned off. A voice over the speakers said, "We need two brave fans to save the show!"

Without thinking, {name2} leapt onto the stage, armed with her {kpop_merch} and {name1} behind her. The crowd chanted their names, and someone handed them microphones made of cotton candy.

💫 Chapter 3: Legends of the Night

They performed a chaotic freestyle that included the {dance_move}, moonwalking with a {snack} in each hand, and dramatic slow-motion karaoke. Somehow, it worked. The stage lights came back on, {idol_name} hugged them both, and confetti exploded in every direction.

As they walked back to their hotel—now minor celebrities—they looked at each other and said, "This was the most {adjective1} day of our lives." And in that exact moment, a fan ran up to them and whispered, “Are you the girls from the glitter cannon incident?”

Legendary. {emoji}
"""

    # Show the final story
    print("\n💥 Your K-pop Concert Adventure 💥")
    print(story)

if __name__ == "__main__":
    play_madlibs()
