word = input("Enter a word: ")
s_word = word.lower()
reverse_word = s_word[::-1]
if s_word == reverse_word:
    print(f"{word} is a palindrome.")
else:
    print(f"{word} is not a palindrome.")