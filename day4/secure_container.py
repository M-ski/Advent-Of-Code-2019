import logging as log
from typing import List


class SecureContainer:
    @staticmethod
    def is_six_digit_number(pwd: int) -> bool:
        return type(pwd) == int and 100000 <= pwd <= 999999

    @staticmethod
    def __split_pwd(pwd: int) -> List[int]:
        return [int(num) for num in str(pwd)]

    @staticmethod
    def __validate_pair(i, nums):
        pair = (nums[i], nums[i - 1])
        is_valid = True
        if i - 2 >= 0 and nums[i - 2] == pair[0]:
            is_valid = False
        if i + 1 < len(nums) and nums[i + 1] == pair[1]:
            is_valid = False
        log.debug("Pair was valid: %s", is_valid)
        return is_valid

    @staticmethod
    def has_two_paired_digits_not_in_larger_set(pwd: int) -> bool:
        nums = SecureContainer.__split_pwd(pwd)
        log.debug('has two paired Digits, nums: %s', nums)
        are_any_pairs_valid = False
        for i in range(1, 6):
            previous_num = nums[i - 1]
            current_num = nums[i]
            if previous_num == current_num:
                log.info('nums had paired digits: %s, pair: (%s,%s)', pwd, previous_num, current_num)
                are_any_pairs_valid = are_any_pairs_valid or SecureContainer.__validate_pair(i, nums)
        return are_any_pairs_valid

    @staticmethod
    def always_increments_numbers(pwd: int) -> bool:
        nums = SecureContainer.__split_pwd(pwd)
        prev_num = nums[0]
        log.debug('do digits increment: %s', nums)
        for num in nums:
            if prev_num > num:
                return False
            prev_num = num
        log.info('digits always incremented in: %s', pwd)
        return True

    @staticmethod
    def is_valid_pwd(pwd: int) -> bool:
        return SecureContainer.is_six_digit_number(pwd) and SecureContainer.always_increments_numbers(pwd) \
               and SecureContainer.has_two_paired_digits_not_in_larger_set(pwd)


def main():
    puzzle_input = (109165, 576723)
    # possible_passwords: List[int] = [pwd for pwd in range(puzzle_input[0], puzzle_input[1]) if isValidPwd(pwd)]
    possible_passwords: List[int] = []
    for pwd in range(puzzle_input[0], puzzle_input[1]):
        if SecureContainer.is_valid_pwd(pwd):
            possible_passwords.append(pwd)
    log.info('Possible number of passwords: %s', len(possible_passwords))
    log.info('Possible passwords: %s', possible_passwords)


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    main()
