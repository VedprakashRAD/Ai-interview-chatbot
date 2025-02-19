from datetime import datetime
import random
import string

class IDService:
    @staticmethod
    def generate_candidate_id() -> str:
        timestamp = datetime.now().strftime("%Y%m%d")
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"CAND{timestamp}{random_chars}"

    @staticmethod
    def generate_test_id() -> str:
        timestamp = datetime.now().strftime("%Y%m%d")
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"TEST{timestamp}{random_chars}" 