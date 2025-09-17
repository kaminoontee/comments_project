import random
import string

def custom_captcha():
    chars = string.ascii_letters + string.digits  # буквы + цифры
    text = "".join(random.choice(chars) for _ in range(5))
    return text, text