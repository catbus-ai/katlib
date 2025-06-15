print("Welcome to the Mad Libs Game! 🤪")

# Ask the player for some words
adjective = input("Enter an adjective: ")
adjective2 = input("Enter an adjective: ")
animal = input("Enter an animal: ")
place = input("Enter a place: ")
verb = input("Enter a verb ending in -ing: ")
silly_word = input("Enter a silly made-up word: ")
friend_name = input("Enter your friend's name: ")

# Create the story
story = f"""
One day, my friend {friend_name} and I were walking through the {adjective} forest.
Suddenly, we saw a {animal} {verb} near a {silly_word} tree! It was so {adjective2}!
We couldn't believe our eyes, so we ran all the way to {place} while laughing our heads off.
It was the best day ever!
"""

# Show the final story
print("\n🎉 Here's your Mad Libs story! 🎉")
print(story)
