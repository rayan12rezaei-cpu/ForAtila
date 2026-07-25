import json

class ProvinceDetector:
    def __init__(self, json_file: str):
        self.provinces_data = self._load_data(json_file)

    def _load_data(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)['provinces']
        except FileNotFoundError:
            print("Can\'t load json | خطا در json")
            return []

    def is_valid_national_code(code: str) -> bool:
        if not (code.isdigit() and len(code) == 10):
            return False
        digits = [int(d) for d in code]
        checksum = sum(digits[i] * (10 - i) for i in range(9))
        remainder = checksum % 11
        if remainder < 2:
            return digits[9] == remainder
        else:
            return digits[9] == (11 - remainder)
  
    def detect(self, national_code: str):
        if not is_valid_national_code(national_code):
            return "not valid | نامعتبر"

        prefix = int(national_code[:3])

        for item in self.provinces_data:
            for start, end in item['ranges']:
                if start <= prefix <= end:
                    return item['name']
        
        return "unknow | نامشخص"

detector = ProvinceDetector('provinces.json')

print(detector.detect(input("Enter National Code | کدملی را وارد کنید:")))
