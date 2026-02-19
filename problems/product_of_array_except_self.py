def func(nums):

    n = len(nums)
    answer = [1] * n

    left_product = 1

    for i in range(n):
        answer[i] = left_product
        left_product *= nums[i]

    right_product = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= right_product
        right_product *= nums[i]

    return answer

'''
Lógica:

--> Para cada posição, o resultado é (produto à esquerda × produto à direita)
--> Faço uma primeira passada acumulando o produto da esquerda
--> Em cada posição, salvo esse produto no array resposta
--> Depois faço uma segunda passada acumulando o produto da direita
--> Multiplico o valor já salvo pelo produto da direita
--> Assim evito divisão e mantenho O(n) tempo e O(1) espaço extra
'''