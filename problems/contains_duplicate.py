def func(nums):
    seen = set()

    for num in nums:
        if num in seen:
            return True
        seen.add(num)

    return False

print(func([1, 2, 3, 1]))

'''
Lógica:

--> Inicio um set vazio
--> Percorro o array e vou adicionando os elementos ao set
--> Se encontrar um elemento que já existe no set, retorna True
--> Caso contrário, retorna False
'''