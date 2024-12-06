# def longestSubarrayWithSumK(arr, k):
#     # Dictionary to store the first occurrence of prefix sums
#     sum_map = {0: -1}
#     prefix_sum = 0
#     max_length = 0
    
#     for i in range(len(arr)):
#         # Update prefix sum
#         prefix_sum += arr[i]
        
#         # Check if (prefix_sum - k) exists in the map
#         required_prefix = prefix_sum - k
#         if required_prefix in sum_map:
#             # Update max_length
#             max_length = max(max_length, i - sum_map[required_prefix])
        
#         # Store the first occurrence of this prefix_sum
#         if prefix_sum not in sum_map:
#             sum_map[prefix_sum] = i
    
#     return max_length

# # Example Usage
# print(longestSubarrayWithSumK([10, 5, 2, 7, 1, 9], 15))  # Output: 4
# print(longestSubarrayWithSumK([-1, 2, -3], -2))          # Output: 3
# print(longestSubarrayWithSumK([1, -1, 5, -2, 3], 3))     # Output: 4
