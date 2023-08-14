import random
import string

def generate_otp(length=6):
    return ''.join(random.choice(string.digits) for _ in range(length))
