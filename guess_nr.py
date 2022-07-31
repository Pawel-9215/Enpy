#we are starting sooo low now....
import random

guessses = 0

print("Hello what is your name?")
user_name = input()

number = random.randint(1, 20)

print(" Welcome there", user_name, "It's a pleasure\n",
        "Im thinking about a number between 1 and 20, try to guess it.\n You have 6 tries")

while guessses <= 6:
    
    print("Give me your guess")
    guess = int(input())

    if guess < number:
        print("Your guess was too low")
    elif guess > number:
        print("Your geuess is too high")
    elif guess == number:
        print("yes, number was", guess, "congratz, you won\n")
        quit()

    guessses += 1
    
    print(f"You have {6-guessses} tries left")
        
print("You lost, you used up all your tries")