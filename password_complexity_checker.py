import re
import math
import secrets
from collections import defaultdict

class Password_Complexity_Checker:
    def __init__(self, password, username="", email="", old_password=""):
        self.password = password
        self.username = username
        self.email = email
        self.old_password = old_password
        self.common_passwords = self._load_common_passwords()
        self.criteria = self._initialize_criteria()
        
    def _load_common_passwords(self):
        """Load common passwords from file or use default list"""
        try:
            with open('common_passwords.txt') as f:
                return [line.strip().lower() for line in f]
        except FileNotFoundError:
            return ["password", "123456", "qwerty", "letmein", "welcome",
                    "admin", "12345678", "123456789", "123123", "111111"]
    
    def _initialize_criteria(self):
        """Initialize all password checking criteria"""
        return {
            "length": len(self.password) >= 12,
            "uppercase": bool(re.search(r"[A-Z]", self.password)),
            "lowercase": bool(re.search(r"[a-z]", self.password)),
            "number": bool(re.search(r"\d", self.password)),
            "special_char": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.password)),
            "not_common": self.password.lower() not in self.common_passwords,
            "no_sequential": not self._has_sequential_chars(),
            "no_repeated": not self._has_repeated_chars(),
            "no_personal_info": not self._contains_personal_info(),
            "not_similar_old": not self._is_similar_to_old(),
            "no_dict_words": not self._contains_dictionary_word(),
            "no_keyboard_patterns": not self._has_keyboard_pattern()
        }
    
    def _has_sequential_chars(self):
        """Check for sequential characters (abc, 123, etc.)"""
        sequences = [
            "abcdefghijklmnopqrstuvwxyz",
            "zyxwvutsrqponmlkjihgfedcba",
            "01234567890",
            "9876543210",
            "qwertyuiop",
            "poiuytrewq",
            "asdfghjkl",
            "lkjhgfdsa",
            "zxcvbnm",
            "mnbvcxz"
        ]
        password_lower = self.password.lower()
        return any(seq in password_lower for seq in sequences)
    
    def _has_repeated_chars(self):
        """Check for repeated characters (aaa, 111)"""
        return re.search(r"(.)\1\1", self.password)
    
    def _contains_personal_info(self):
        """Check for personal information in password"""
        if not self.username and not self.email:
            return False
        personal_info = []
        if self.username:
            personal_info.append(self.username.lower())
        if self.email:
            personal_info.append(self.email.split("@")[0].lower())
        return any(info in self.password.lower() for info in personal_info)
    
    def _is_similar_to_old(self):
        """Check similarity with old password"""
        if not self.old_password:
            return False
        return self.password.lower() == self.old_password.lower() or \
               self.old_password.lower() in self.password.lower()
    
    def _contains_dictionary_word(self):
        """Check for dictionary words"""
        try:
            with open('/usr/share/dict/words') as f:
                dictionary = set(word.strip().lower() for word in f)
        except FileNotFoundError:
            return False
        return any(word in self.password.lower() for word in dictionary if len(word) > 3)
    
    def _has_keyboard_pattern(self):
        """Check for keyboard patterns"""
        keyboard_rows = [
            "qwertyuiop",
            "asdfghjkl",
            "zxcvbnm",
            "1234567890"
        ]
        password_lower = self.password.lower()
        for row in keyboard_rows:
            for i in range(len(row) - 3):
                if row[i:i+4] in password_lower or row[i:i+4][::-1] in password_lower:
                    return True
        return False
    
    def calculate_entropy(self):
        """Calculate password entropy in bits"""
        pool_size = 0
        if re.search(r'[a-z]', self.password): pool_size += 26
        if re.search(r'[A-Z]', self.password): pool_size += 26
        if re.search(r'\d', self.password): pool_size += 10
        if re.search(r'[^a-zA-Z0-9]', self.password): pool_size += 32
        
        return math.log2(pool_size ** len(self.password)) if pool_size else 0
    
    def analyze(self):
        """Perform complete password analysis"""
        score = sum(self.criteria.values())
        total_criteria = len(self.criteria)
        entropy = self.calculate_entropy()
        
        strength = self._get_strength_label(score, entropy)
        
        return {
            "score": score,
            "total_possible": total_criteria,
            "strength": strength,
            "entropy": entropy,
            "is_strong": score >= total_criteria * 0.75,
            "failed_checks": [k for k, v in self.criteria.items() if not v]
        }
    
    @staticmethod
    def _get_strength_label(score, entropy):
        """Determine strength label based on score and entropy"""
        if score >= 10 and entropy >= 75:
            return "excellent"
        elif score >= 8 and entropy >= 60:
            return "very_strong"
        elif score >= 6 and entropy >= 45:
            return "strong"
        elif score >= 4 and entropy >= 30:
            return "moderate"
        elif score >= 2:
            return "weak"
        else:
            return "very_weak"

def get_password_input():
    """Get password input from user"""
    print("Enter password to analyze: ")
    try:
        import getpass
        return getpass.getpass()
    except Exception:
        return input()

def create_secure_password():
    """Generate a secure password suggestion"""
    adjectives = ["Red", "Blue", "Happy", "Secure", "Strong"]
    nouns = ["Dragon", "Coffee", "Mountain", "Shield", "Castle"]
    special = secrets.choice("!@#$%^&*")
    number = f"{secrets.randbelow(90) + 10:02d}"
    return f"{secrets.choice(adjectives)}{secrets.choice(nouns)}{number}{special}"

def main():
    """Main execution function"""
    password = get_password_input()
    if not password:
        print("Error: Password cannot be empty")
        return
    
    analyzer = Password_Complexity_Checker(password)
    result = analyzer.analyze()
    
    print("\nPassword Analysis Results:")
    print(f"Strength: {result['strength'].replace('_', ' ').title()}")
    print(f"Score: {result['score']}/{result['total_possible']}")
    print(f"Entropy: {result['entropy']:.1f} bits")
    
    if result['failed_checks']:
        print("\nFailed Checks:")
        for check in result['failed_checks']:
            print(f"- {check.replace('_', ' ').title()}")
    
    if not result['is_strong']:
        print(f"\nSuggested secure password: {create_secure_password()}")

if __name__ == "__main__":
    main()import re
import math
import secrets
from collections import defaultdict

class Password_Complexity_Checker:
    def __init__(self, password, username="", email="", old_password=""):
        self.password = password
        self.username = username
        self.email = email
        self.old_password = old_password
        self.common_passwords = self._load_common_passwords()
        self.criteria = self._initialize_criteria()
        
    def _load_common_passwords(self):
        """Load common passwords from file or use default list"""
        try:
            with open('common_passwords.txt') as f:
                return [line.strip().lower() for line in f]
        except FileNotFoundError:
            return ["password", "123456", "qwerty", "letmein", "welcome",
                    "admin", "12345678", "123456789", "123123", "111111"]
    
    def _initialize_criteria(self):
        """Initialize all password checking criteria"""
        return {
            "length": len(self.password) >= 12,
            "uppercase": bool(re.search(r"[A-Z]", self.password)),
            "lowercase": bool(re.search(r"[a-z]", self.password)),
            "number": bool(re.search(r"\d", self.password)),
            "special_char": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.password)),
            "not_common": self.password.lower() not in self.common_passwords,
            "no_sequential": not self._has_sequential_chars(),
            "no_repeated": not self._has_repeated_chars(),
            "no_personal_info": not self._contains_personal_info(),
            "not_similar_old": not self._is_similar_to_old(),
            "no_dict_words": not self._contains_dictionary_word(),
            "no_keyboard_patterns": not self._has_keyboard_pattern()
        }
    
    def _has_sequential_chars(self):
        """Check for sequential characters (abc, 123, etc.)"""
        sequences = [
            "abcdefghijklmnopqrstuvwxyz",
            "zyxwvutsrqponmlkjihgfedcba",
            "01234567890",
            "9876543210",
            "qwertyuiop",
            "poiuytrewq",
            "asdfghjkl",
            "lkjhgfdsa",
            "zxcvbnm",
            "mnbvcxz"
        ]
        password_lower = self.password.lower()
        return any(seq in password_lower for seq in sequences)
    
    def _has_repeated_chars(self):
        """Check for repeated characters (aaa, 111)"""
        return re.search(r"(.)\1\1", self.password)
    
    def _contains_personal_info(self):
        """Check for personal information in password"""
        if not self.username and not self.email:
            return False
        personal_info = []
        if self.username:
            personal_info.append(self.username.lower())
        if self.email:
            personal_info.append(self.email.split("@")[0].lower())
        return any(info in self.password.lower() for info in personal_info)
    
    def _is_similar_to_old(self):
        """Check similarity with old password"""
        if not self.old_password:
            return False
        return self.password.lower() == self.old_password.lower() or \
               self.old_password.lower() in self.password.lower()
    
    def _contains_dictionary_word(self):
        """Check for dictionary words"""
        try:
            with open('/usr/share/dict/words') as f:
                dictionary = set(word.strip().lower() for word in f)
        except FileNotFoundError:
            return False
        return any(word in self.password.lower() for word in dictionary if len(word) > 3)
    
    def _has_keyboard_pattern(self):
        """Check for keyboard patterns"""
        keyboard_rows = [
            "qwertyuiop",
            "asdfghjkl",
            "zxcvbnm",
            "1234567890"
        ]
        password_lower = self.password.lower()
        for row in keyboard_rows:
            for i in range(len(row) - 3):
                if row[i:i+4] in password_lower or row[i:i+4][::-1] in password_lower:
                    return True
        return False
    
    def calculate_entropy(self):
        """Calculate password entropy in bits"""
        pool_size = 0
        if re.search(r'[a-z]', self.password): pool_size += 26
        if re.search(r'[A-Z]', self.password): pool_size += 26
        if re.search(r'\d', self.password): pool_size += 10
        if re.search(r'[^a-zA-Z0-9]', self.password): pool_size += 32
        
        return math.log2(pool_size ** len(self.password)) if pool_size else 0
    
    def analyze(self):
        """Perform complete password analysis"""
        score = sum(self.criteria.values())
        total_criteria = len(self.criteria)
        entropy = self.calculate_entropy()
        
        strength = self._get_strength_label(score, entropy)
        
        return {
            "score": score,
            "total_possible": total_criteria,
            "strength": strength,
            "entropy": entropy,
            "is_strong": score >= total_criteria * 0.75,
            "failed_checks": [k for k, v in self.criteria.items() if not v]
        }
    
    @staticmethod
    def _get_strength_label(score, entropy):
        """Determine strength label based on score and entropy"""
        if score >= 10 and entropy >= 75:
            return "excellent"
        elif score >= 8 and entropy >= 60:
            return "very_strong"
        elif score >= 6 and entropy >= 45:
            return "strong"
        elif score >= 4 and entropy >= 30:
            return "moderate"
        elif score >= 2:
            return "weak"
        else:
            return "very_weak"

def get_password_input():
    """Get password input from user"""
    print("Enter password to analyze: ")
    try:
        import getpass
        return getpass.getpass()
    except Exception:
        return input()

def create_secure_password():
    """Generate a secure password suggestion"""
    adjectives = ["Red", "Blue", "Happy", "Secure", "Strong"]
    nouns = ["Dragon", "Coffee", "Mountain", "Shield", "Castle"]
    special = secrets.choice("!@#$%^&*")
    number = f"{secrets.randbelow(90) + 10:02d}"
    return f"{secrets.choice(adjectives)}{secrets.choice(nouns)}{number}{special}"

def main():
    """Main execution function"""
    password = get_password_input()
    if not password:
        print("Error: Password cannot be empty")
        return
    
    analyzer = Password_Complexity_Checker(password)
    result = analyzer.analyze()
    
    print("\nPassword Analysis Results:")
    print(f"Strength: {result['strength'].replace('_', ' ').title()}")
    print(f"Score: {result['score']}/{result['total_possible']}")
    print(f"Entropy: {result['entropy']:.1f} bits")
    
    if result['failed_checks']:
        print("\nFailed Checks:")
        for check in result['failed_checks']:
            print(f"- {check.replace('_', ' ').title()}")
    
    if not result['is_strong']:
        print(f"\nSuggested secure password: {create_secure_password()}")

if __name__ == "__main__":
    main()
