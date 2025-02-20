import random
import string
from .models import URLTransform

def generate_short_code(min_length=5, max_length=20):
    characters = string.ascii_letters + string.digits
  
    for length in range(min_length, max_length + 1):
        short_code = ''.join(random.choices(characters, k=length))
        if not URLTransform.objects.filter(short_code=short_code).exists():
            return short_code
    
    raise Exception("Generate a unique short code is failed")