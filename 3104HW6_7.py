import array
import math
import sys

# Mr E growing magic beans and wants to grow specific lengths of bean stalks
# He starts with a 1 inch cutting and each day applies one drop of fertilizer
# making it grow either 1, 4, 5, or 11 inches depending on the type of fertilizer
# He wishes to get a bean stalk onf length n using the minimum number of drops of fertilizer
# He doesn't want to cut the finished stalk (cannot shorten a stalk)
# Goal is to use dynamic programming to find out how to grow a stalk of length n
# from a stalk of length 1 using the least number of steps

# Write recurrence minDrops(j, n) that represents the minimum number of drops of fertilizer
# to grow a stalk from j inches to n inches
def minDrops(j, n):
    if j == n:
        return 0
    if j > n:
        return float('inf')  # Impossible case

    # Possible growths
    growths = [1, 4, 5, 11]
    min_drops = float('inf') # initialize to infinity

    for growth in growths:
        drops = minDrops(j + growth, n) # recursive call
        if drops != float('inf'):
            min_drops = min(min_drops, drops + 1) # update min drops

    return min_drops if min_drops != float('inf') else -1
    #raise NotImplementedError("Function not yet implemented")

# Example usage:
n = 43
#print(f"Minimum drops to grow from 1 to {n} inches:", minDrops(1, n))  # Output: Minimum drops

# memoize the recurrence
# assume that n is fixed
# assume that j = 1 is the starting point
# the memo table T[0], ..., T[n] should store the value of minDrops(j, n)
def minDrops_Memoize(n):
    T = [-1] * (n + 1) # initialize memoization table

    def helper(j):
        if j == n:
            return 0
        if j > n:
            return float('inf')  # Impossible case
        if T[j] != -1: # check if already computed
            return T[j]

        growths = [1, 4, 5, 11]
        min_drops = float('inf')

        for growth in growths:
            drops = helper(j + growth) # recursive call
            if drops != float('inf'):
                min_drops = min(min_drops, drops + 1) # update min drops

        T[j] = min_drops if min_drops != float('inf') else -1 # store result
        return T[j]

    return helper(1)
    #raise NotImplementedError("Function not yet implemented")

# Example usage:
n = 43
#print(f"Minimum drops to grow from 1 to {n} inches with memoization:", minDrops_Memoize(n))  # Output: Minimum drops with memoization


# Modify solution from memoization to return which fertilizer to use at each step
# Answer must be a pair: (min number of total drops, list of fertilizers per drop "1, 4, 5, or 11")
def minDrops_Solution(n):
    T = [-1] * (n + 1)
    choice = [-1] * (n + 1)

    def helper(j):
        if j == n:
            return 0
        if j > n:
            return float('inf')  # Impossible case
        if T[j] != -1:
            return T[j]

        growths = [1, 4, 5, 11]
        min_drops = float('inf') # initialize to infinity
        best_growth = -1

        for growth in growths:
            drops = helper(j + growth)
            if drops != float('inf') and drops + 1 < min_drops: # found a better option
                min_drops = drops + 1
                best_growth = growth # record the best growth choice

        T[j] = min_drops if min_drops != float('inf') else -1 # store the result
        choice[j] = best_growth
        return T[j] # return minimum drops

    total_drops = helper(1) # start from length 1
    if total_drops == -1:
        return (-1, []) # impossible case

    # Reconstruct the list of fertilizers used
    fertilizers = []
    current_length = 1
    while current_length < n:
        fertilizers.append(choice[current_length]) # append chosen fertilizer
        current_length += choice[current_length] # move to the next length

    return (total_drops, fertilizers)
    #raise NotImplementedError("Function not yet implemented")

# Example usage:
n = 43
result = minDrops_Solution(n)
#print(f"Minimum drops and fertilizers to grow from 1 to {n} inches:", result)  # Output: Minimum drops and fertilizers


# Mr E noticed that any bean stalk length that leaves a remainder of 2 when divided by 7 dies over night
# Modify the algorithm to avoid these "dead lenghts"
# Write minGoodDrops(j, n) recurrence that represents the minimum number of drops of fertilizer
# necessary to grow a bean stalk from j inches to n inches, avoiding any intermediate stage of length k when k mod 7 = 2
def minGoodDrops(j, n):
    if j == n:
        return 0
    if j > n or j % 7 == 2:
        return float('inf')  # Impossible case

    growths = [1, 4, 5, 11]
    min_drops = float('inf') # initialize to infinity

    for growth in growths:
        drops = minGoodDrops(j + growth, n) # recursive call
        if drops != float('inf'):
            min_drops = min(min_drops, drops + 1) # update min drops

    return min_drops if min_drops != float('inf') else -1
    #raise NotImplementedError("Function not yet implemented")

# Example usage:
n = 43
#print(f"Minimum good drops to grow from 1 to {n} inches:", minGoodDrops(1, n))  # Output: Minimum good drops

# memoize the recurrence in minGoodDrops
def minGoodDrops_Memoize(n):
    T = [-1] * (n + 1) # initialize memoization table

    def helper(j):
        if j == n:
            return 0
        if j > n or j % 7 == 2:
            return float('inf')  # Impossible case
        if T[j] != -1: # check if already computed
            return T[j]

        growths = [1, 4, 5, 11]
        min_drops = float('inf')

        for growth in growths:
            drops = helper(j + growth) # recursive call
            if drops != float('inf'):
                min_drops = min(min_drops, drops + 1) # update min drops

        T[j] = min_drops if min_drops != float('inf') else -1 # store result
        return T[j]

    return helper(1)
    #raise NotImplementedError("Function not yet implemented")

# Example usage:
n = 43
#print(f"Minimum good drops to grow from 1 to {n} inches with memoization:", minGoodDrops_Memoize(n))  # Output: Minimum good drops with memoization


# recover solution in terms of the growth from each drop of fertilizer
def minGoodDrops_Solution(n):
    T = [-1] * (n + 1)
    choice = [-1] * (n + 1)

    def helper(j):
        if j == n:
            return 0
        if j > n or j % 7 == 2:
            return float('inf')  # Impossible case
        if T[j] != -1:
            return T[j]

        growths = [1, 4, 5, 11]
        min_drops = float('inf') # initialize to infinity
        best_growth = -1

        for growth in growths:
            drops = helper(j + growth)
            if drops != float('inf') and drops + 1 < min_drops: # found a better option
                min_drops = drops + 1
                best_growth = growth # record the best growth choice

        T[j] = min_drops if min_drops != float('inf') else -1 # store the result
        choice[j] = best_growth
        return T[j] # return minimum drops

    total_drops = helper(1) # start from length 1
    if total_drops == -1:
        return (-1, []) # impossible case

    # Reconstruct the list of fertilizers used
    fertilizers = []
    current_length = 1
    while current_length < n:
        fertilizers.append(choice[current_length]) # append chosen fertilizer
        current_length += choice[current_length] # move to the next length

    return (total_drops, fertilizers)
    #raise NotImplementedError("Function not yet implemented")

# Example usage:
n = 812
result = minGoodDrops_Solution(n)
#print(f"Minimum good drops and fertilizers to grow from 1 to {n} inches:", result)  # Output: Minimum good drops and fertilizers


# growth on a budget
# Mr E has a budget of daily growth and cost 
# (1 inch for 1 dollar, 4 inches for 2 dollars, 5 inches for 3 dollars, 11 inches for 7 dollars)
# Given n and initial investment D0, plan how Mr E can grow an n inch bean stalk 
# while avoiding dead lengths and staying within budget
# write recurrence minDropsWithBudget(j, d, n) given stalk of length j, budget d
# returns minimum number of drops to grow to n inches
# while avoiding any intermediate stage of length k when k mod 7 = 2
# and not exceeding budget d
# print(minDropsWithBudget(1, 18, 31)) must be 7
# print(minDropsWithBudget(1, 35, 60)) must be 12
# two variables will change and the memotabale must be two dimensional
# The final budget should strictly be above zero because Mr E doesn't want to go bankrupt
def minDropsWithBudget(j, d, n):
    # The final budget should strictly be above zero because Mr E doesn't want to go bankrupt
    if j == n: # base case: reached desired length
        return 0
    if n < j: # impossible case: exceeded desired length
        return float('inf')
    
    growths = [1, 4, 5, 11]
    costs = [1, 2, 3, 7]
    min_drops = float('inf') # initialize to infinity

    # try each type of fertilizer
    for growth, cost in zip(growths, costs):
        new_length = n - growth
        new_budget = d - cost

        if new_length % 7 != 2 and new_budget > 0: # skip dead lengths and ensure budget is positive
            num_drops = 1 + minDropsWithBudget(j, new_budget, new_length) # recursive call
            min_drops = min(min_drops, num_drops) # update minimum drops

    return min_drops
    #raise NotImplementedError("Function not yet implemented")

# Example usage:
D0 = 35
n = 60
#print(f"Minimum drops to grow from 1 to {n} inches with budget {D0}:", minDropsWithBudget(1, D0, n))  # Output: Minimum drops with budget


# write memo table to memoize minDropsWithBudget recurrence
# memo table T[j][d] for j ranging from 1 to n and d ranging from 0 to D
# handle base cases carefully
# answer must coincide with the recursive version minDropsWithBudget

def minDropsWithBudget_Memoize(D, n):
    memo = {} # initialize memoization table

    def helper(d, target):
        if (d, target) in memo: # check if already computed
            return memo[(d, target)]
        if target == 1: # base case: reached desired length
            return 0
        if target < 1: # impossible case: exceeded desired length
            return float('inf')
        
        growths = [1, 4, 5, 11]
        costs = [1, 2, 3, 7]
        min_drops = float('inf') # initialize to infinity

        # try each type of fertilizer
        for growth, cost in zip(growths, costs):
            prev_length = target - growth
            remaining_budget = d - cost

            if prev_length % 7 != 2 and remaining_budget > 0: # skip dead lengths and ensure budget is positive
                drops = helper(remaining_budget, prev_length) # recursive call
                if drops != float('inf'):
                    min_drops = min(min_drops, drops + 1) # update min drops

        
        memo[(d, target)] = min_drops # store result
        return min_drops
    
    return helper(D, n) # return the minimum drops
    #raise NotImplementedError("Function not yet implemented")

# Example usage:
D0 = 35
n = 60
#print(f"Minimum drops to grow from 1 to {n} inches with budget {D0} using memoization:", minDropsWithBudget_Memoize(D0, n))  # Output: Minimum drops with budget using memoization


# Recover the solution (forward DP to avoid dead lengths)
# Return min number of drops and list of fertilizers (in order) that achieve it
def minDropsWithBudget_Solution(D, n):
    growths = [1, 4, 5, 11]
    costs = [1, 2, 3, 7]
    memo = {}   # (j, d) -> min drops from length j with budget d
    choice = {} # (j, d) -> chosen growth

    def helper(j, d):
        # If reached target, require final budget strictly > 0
        if j == n:
            return 0 if d > 0 else float('inf')
        # invalid states
        if j > n or d <= 0 or j % 7 == 2:
            return float('inf')
        if (j, d) in memo:
            return memo[(j, d)]

        best = float('inf')
        best_growth = None
        for growth, cost in zip(growths, costs):
            nj = j + growth
            nd = d - cost
            # skip if immediate next length is dead or budget would be non-positive
            if nd <= 0:
                continue
            if nj % 7 == 2 and nj != n:  # disallow dead intermediate lengths (allow if it's the final target handled above)
                continue
            res = helper(nj, nd)
            if res != float('inf') and res + 1 < best:
                best = res + 1
                best_growth = growth

        memo[(j, d)] = best
        choice[(j, d)] = best_growth
        return best

    total = helper(1, D)
    if total == float('inf'):
        return (-1, [])

    # Reconstruct forward sequence
    seq = []
    j, d = 1, D
    while j < n:
        g = choice.get((j, d))
        if g is None:
            break
        seq.append(g)
        d -= {1:1, 4:2, 5:3, 11:7}[g]
        j += g

    return (total, seq)
    #raise NotImplementedError("Function not yet implemented")

# Example usage:
D0 = 35
n = 60
result = minDropsWithBudget_Solution(D0, n) #result should be 5, [4, 5, 4, 5, 11]
print(f"Minimum drops and fertilizers to grow from 1 to {n} inches with budget {D0}:", result)  # Output: Minimum drops and fertilizers with budget


# end of Mr E's bean stalk problems
#-------------------------------------------------