import time
import sys
import itertools
import string
import matplotlib.pyplot as plt
from getpass import getpass

# Spinner animation characters
spinner = itertools.cycle(['|', '/', '-', '\\'])

# Charset used for brute force (feel free to make this user-selectable later)
charset = string.ascii_letters + string.digits + string.punctuation

# Get password input from user (hidden input)
password = getpass("Enter your password (input is hidden): ")

# Setup
result = ['_'] * len(password)
attempts = 0
guesses_per_char = []

print("\nBrute forcing...\n")

# Brute force loop
for i in range(len(password)):
    char_attempts = 0
    for guess in charset:
        attempts += 1
        char_attempts += 1

        # Spinner + current guess + total attempts
        sys.stdout.write(f"\r[{next(spinner)}] Attempt #{attempts}  -->  " + ''.join(result[:i]) + guess + ''.join(result[i+1:]))
        sys.stdout.flush()

    #NOW FOR THE FUN PART PLAY AROUND WITH THIS SLEEP FUNCTION!
        time.sleep(0.00001)

        if guess == password[i]:
            result[i] = guess
            guesses_per_char.append(char_attempts)
            break

# Final display
print("\n\n Password cracked: " + ''.join(result))
print(f" Total attempts: {attempts}\n")

