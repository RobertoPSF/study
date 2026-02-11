def func(s, t):
    if len(s) != len(t):
        return False
    
    count = {chr(i): 0 for i in range(ord('a'), ord('z') + 1)}

    for c in s:
        count[c] += 1

    for c in t:
        count[c] -= 1
        if count[c] < 0:
            return False
        
    return True
        

print(func("anagram", "nagaram"))


'''
Lógica:

--> Se os tamanhos são diferentes, já falhou
--> Inicializo um contador para cada letra
--> Incremento contagem para cada caractere da primeira string
--> Decremento para cada caractere da segunda
--> Se alguma contagem ficar negativa, não é anagrama
'''