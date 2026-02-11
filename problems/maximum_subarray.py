def func(nums):

    current_sum = nums[0]
    max_sum = nums[0]

    for x in nums[1:]:
        current_sum = max(x, current_sum + x)
        max_sum = max(current_sum, max_sum)

    return max_sum


print(func([-2,1,-3,4,-1,2,1,-5,4]))


'''
Lógica:

--> Começo com o primeiro elemento
--> Para cada número:
        ou começo um novo subarray
        ou estendo o anterior
--> Escolho sempre a opção que maximiza a soma atual
--> Mantenho o melhor valor já visto
'''