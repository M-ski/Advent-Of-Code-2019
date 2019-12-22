from unittest import TestCase

from day4.secure_container import SecureContainer


class SecureContainerTests(TestCase):

    def test_valid_pwd_length_valid(self):
        self.assertTrue(SecureContainer.is_six_digit_number(100000))
        self.assertTrue(SecureContainer.is_six_digit_number(123456))
        self.assertTrue(SecureContainer.is_six_digit_number(999999))

    def test_valid_pwd_length_too_short(self):
        too_short: int = 1000
        self.assertFalse(SecureContainer.is_six_digit_number(too_short))

    def test_valid_pwd_length_too_long(self):
        too_long: int = 10000000
        self.assertFalse(SecureContainer.is_six_digit_number(too_long))

    def test_valid_pwd_length_None(self):
        self.assertFalse(SecureContainer.is_six_digit_number(None))
        self.assertFalse(SecureContainer.is_six_digit_number(""))
        self.assertFalse(SecureContainer.is_six_digit_number([]))

    def test_always_increments_numbers(self):
        self.assertTrue(SecureContainer.always_increments_numbers(123456))

    def test_always_increments_numbers_numbers_are_the_same(self):
        self.assertTrue(SecureContainer.always_increments_numbers(111111))
        self.assertTrue(SecureContainer.always_increments_numbers(999999))

    def test_always_increment_numbers_pairs_are_present(self):
        self.assertTrue(SecureContainer.always_increments_numbers(112233))

    def test_always_increment_numbers_not_true(self):
        self.assertFalse(SecureContainer.always_increments_numbers(987654))  # decrementing series
        self.assertFalse(SecureContainer.always_increments_numbers(123454))  # last number decrement

    def test_has_two_paired_digits_not_in_larger_set(self):
        self.assertTrue(SecureContainer.has_two_paired_digits_not_in_larger_set(112233))
        self.assertTrue(SecureContainer.has_two_paired_digits_not_in_larger_set(123455))

    def test_has_two_paired_digits_not_in_larger_set_pair_is_in_larger_set(self):
        self.assertFalse(SecureContainer.has_two_paired_digits_not_in_larger_set(123333))  # larger set of 4
        self.assertFalse(SecureContainer.has_two_paired_digits_not_in_larger_set(111222))  # two larger sets of three
        self.assertFalse(SecureContainer.has_two_paired_digits_not_in_larger_set(111234))  # one larger set at start
        self.assertFalse(SecureContainer.has_two_paired_digits_not_in_larger_set(123444))  # one larger set at end
        self.assertFalse(SecureContainer.has_two_paired_digits_not_in_larger_set(123334))  # one larger set in middle

    def test_has_two_paired_digits_not_in_larger_set_one_pair_one_in_larger_set(self):
        self.assertTrue(SecureContainer.has_two_paired_digits_not_in_larger_set(111122))  # regular pair after l. set
