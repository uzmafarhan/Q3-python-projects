# Fill out print_multiple(message, repeats), which takes as parameters a string message to print, 
# and an integer repeats number of times to print message. 
# We've written the main() function for you, which prompts the user for a message and a number of repeats.

# Here's a sample run of the program (user input is in blue):

# Please type a message: Hello! Enter a number of times to repeat your message: 6 Hello! Hello! Hello! Hello! Hello! Hello!

def print_multiple(message, repeats):
    for _ in range(repeats):
        print(message)

def main():
    message = input("Please type a message: ")
    repeats = int(input("Enter a number of times to repeat your message: "))
    print_multiple(message, repeats)

main()
# Note: The print_multiple function takes a string message and an integer repeats as parameters.
# It prints the message the specified number of times. The main function prompts the user for input and calls print_multiple.