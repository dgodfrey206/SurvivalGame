# guess number

class Solution:
    def __init__(self, r_n):
        self.r = r_n
    def guess(self, n):
        if n < self.r:
            return 1
        elif n > self.r:
            return -1
        return 0

    def guessNumber(self, nums):
        l, r = 0, len(nums) - 1

        while l <= r:
            m = (l + r) // 2
            g = self.guess(nums[m])
            if g == -1:
                r = m - 1
            elif g == 1:
                l = m + 1
            else:
                return nums[m]
        return -1
    
s = Solution(10)

print(s.guessNumber([i for i in range(12)]))
