import random
import io
from captcha.image import ImageCaptcha

def generate_captcha() -> tuple[io.BytesIO, int]:
    randint = random.randint(10000, 99999)
    image_captcha = ImageCaptcha(width=280, height=90)
    data = image_captcha.generate(str(randint))
    buf = io.BytesIO(data.read())
    buf.seek(0)
    return buf, randint