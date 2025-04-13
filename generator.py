import random
import string

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    if length < sum([use_upper, use_lower, use_digits, use_special]):
        raise ValueError("Password length too short for the selected options!")

    char_sets = []
    password_chars = []

    if use_upper:
        char_sets.append(string.ascii_uppercase)
        password_chars.append(random.choice(string.ascii_uppercase))

    if use_lower:
        char_sets.append(string.ascii_lowercase)
        password_chars.append(random.choice(string.ascii_lowercase))

    if use_digits:
        char_sets.append(string.digits)
        password_chars.append(random.choice(string.digits))

    if use_special:
        char_sets.append(string.punctuation)
        password_chars.append(random.choice(string.punctuation))

    # Fill remaining length with random choices from all selected pools
    all_chars = ''.join(char_sets)
    remaining_length = length - len(password_chars)
    password_chars += random.choices(all_chars, k=remaining_length)

    # Shuffle to avoid predictable placement
    random.shuffle(password_chars)

    return ''.join(password_chars)

def password_strength(password):
    length = len(password)
    score = 0

    # Scoring rules
    if length >= 12:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    # Strength meter
    if score <= 2:
        return "Weak "
    elif score == 3:
        return "Moderate "
    elif score == 4:
        return "Strong "
    else:
        return "Unbreakable "

def get_user_input():
    print("🔐 Welcome to the Password Generator 🔐")
    try:
        length = int(input("Enter desired password length (e.g., 16): "))
    except ValueError:
        print("Not a valid number. Defaulting to 12.")
        length = 12

    print("Include the following in your password:")
    use_upper = input("Uppercase letters? (Y/n): ").strip().lower() != 'n'
    use_lower = input("Lowercase letters? (Y/n): ").strip().lower() != 'n'
    use_digits = input("Digits? (Y/n): ").strip().lower() != 'n'
    use_special = input("Special characters (e.g. @#$%)? (Y/n): ").strip().lower() != 'n'

    return length, use_upper, use_lower, use_digits, use_special

def main():
    length, use_upper, use_lower, use_digits, use_special = get_user_input()

    try:
        password = generate_password(length, use_upper, use_lower, use_digits, use_special)
        strength = password_strength(password)

        print(f"\n🎉 Your generated password:\n{password}")
        print(f"🔎 Strength: {strength}")

        if CLIPBOARD_AVAILABLE:
            copy = input("Copy password to clipboard? (Y/n): ").strip().lower()
            if copy != 'n':
                pyperclip.copy(password)
                print("✅ Password copied to clipboard!")
        else:
            print("(Install 'pyperclip' to enable clipboard support.)")

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()
