class Solution:
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        dic_result = []
        result = []
        dic = {}
        for i in range(len(nums)):
            dic[i] = nums[i]
            for j in range(len(nums))[i + 1:]:
                dic[j] = nums[j]
                for k in range(len(nums))[j + 1:]:
                    if dic[i] + dic[j] + nums[k] == 0:
                        dic[k] = nums[k]
                        if dic not in dic_result and dic != {}:
                            dic_result.append(dic)
                    if k == len(nums) - 1:
                        if dic.get(k):
                            dic.pop(k)
                        break
                dic.pop(j)
            dic.clear()
        for s in dic_result:
            result.append(s.values())
        return result


s = Solution()
print(s.threeSum([-1, 0, 1, 2, -1, -4]))
