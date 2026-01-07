import random
from captcha.image import ImageCaptcha

def generate_captcha() -> bytes:
    randint = random.randint(10000, 99999)
    image_captcha = ImageCaptcha(width=280, height=90)
    data = image_captcha.generate(str(randint))
    return data.read()