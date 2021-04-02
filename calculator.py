from collections import deque # Fiquei em duvida entre usar uma deque ou uma stack de um pacote externo e usei os 2
from pythonds.basic import Stack


class Calc:
    items = deque()
    variables = {}
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3} # Ordem de prioridade das operações

    @staticmethod
    def calc(user_input):
        identifier = user_input.split()[0]
        if not identifier.isalpha() and not identifier.isnumeric(): # Checando se o identificador é valido (Para dar assign em uma variavel)
            print('Invalid identifier')
            return
        try:
            nums = ' '.join(Calc.variables.get(x) if x.isalpha() else x for x in user_input.split()) 
            print(Calc.postfixToResult(Calc.toPostfix(nums))) # Chamando as funções de calculo geral ja no print()
        except TypeError: # excessao para qualquer TypeError é por variavel invalida
            print('Unknown variable') 
        except Exception: # Qualquer outra excessao é criado pelo input do usuario ou manipulação deste
            print('Invalid Expression')

    @staticmethod
    def postfixToResult(postfixExpr): # Calculo da expressão convertida em postfix
        operandStack = Stack()
        tokenList = postfixExpr.split()

        for token in tokenList:
            if token.isdigit():
                operandStack.push(int(token))
            else:
                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                result = eval(str(operand1) + str(token) + str(operand2))
                operandStack.push(result)
        return int(operandStack.pop())

    @staticmethod
    def declare_variable(user_input): # Metodo pra declaração de variavel do usuario
        var, eq, val = user_input.partition('=')
        var, val = var.strip(), val.strip()
        if not var.isalpha():
            print('Invalid identifier')
            return
        if not (val.isalpha() or val.isnumeric()) or\
                val.isalpha() and not Calc.variables.get(val):
            print('Invalid assignment')
            return
        Calc.variables[var] = val if val.isnumeric() else Calc.variables.get(val)

    @staticmethod
    def toPostfix(infixexpr): # Conversão da expressão entrada pelo usuario para PostFix
        prec = {"^": 4, "*": 3, "/": 3, "+": 2, "-": 2, "(": 1}
        opStack = Stack()
        postfixList = []
        temporary = infixexpr.split()
        tokenList = []
        for i in temporary: # O Split só separa por 1 argumento e sendo ele " " eu tive que filtrar melhor a lista
            if "(" in i and i != "(":
                tokenList.append("(")
                tokenList.append(i.strip("("))
            elif ")" in i and i != ")":
                tokenList.append(i.strip(")"))
                tokenList.append(")")
            elif "*" in i and len(i) > 1:
                tokenList.append(",.;")
            elif "/" in i and len(i) > 1:
                tokenList.append(",.;")
            else:
                tokenList.append(i)
        for token in tokenList:
            if token.isdigit():
                postfixList.append(token)
            elif token.isalpha():
                postfixList.append(Calc.variables[token])
            elif token == '(':
                opStack.push(token)
            elif token == ')':
                topToken = opStack.pop()
                while topToken != '(':
                    postfixList.append(topToken)
                    topToken = opStack.pop()
            else:
                while (not opStack.isEmpty()) and (prec[opStack.peek()] >= prec[token]):
                    postfixList.append(opStack.pop())
                opStack.push(token)

        while not opStack.isEmpty():
            postfixList.append(opStack.pop())
        return " ".join(postfixList)


def main(): # main que sustenta o programa e aceita os /comands 
    calc = Calc()
    while True:
        user_input = input()
        if user_input == '/exit':
            print('Bye!')
            exit()
        elif user_input == '/help':
            print('A bit of a smart calculator')
            continue
        elif user_input.startswith('/'):
            print('Unknown command')
            continue
        elif user_input.find('=') != -1:
            calc.declare_variable(user_input)
        elif user_input:
            calc.calc(user_input)


if __name__ == '__main__':
    main()
