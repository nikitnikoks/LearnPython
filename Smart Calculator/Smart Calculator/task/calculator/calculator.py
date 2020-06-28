import operator


def return_value(indata, variables):
    indata = indata.strip(' ')

    # return value if indata is variable
    if indata in variables.keys():
        return variables[indata]
    # display entered value if indata is digit
    elif indata.isdigit():
        return indata
    # return error if entered unknown variable
    elif indata.isalpha():
        raise NameError
    # return error if digits and letters in indata
    elif len([char for char in indata if char.isdigit()]) > 0 \
            and len([char for char in indata if char.isalpha()]) > 0:
        raise TypeError
    else:
        raise ValueError


# create variable
def define_variable(indata, variables):
    parsed_data = indata.split('=')
    parsed_data = list(element.strip() for element in parsed_data if element != '')  # remove duplicate spaces

    variable_name = parsed_data[0]
    variable_value = parsed_data[1]

    # take variable value from existing variable if any
    for key in variables.keys():
        if key == variable_value:
            variable_value = variables[key]

    # return error if digit in name
    if any(char.isdigit() for char in variable_name):
        raise NameError
    # return error is too many arguments or digits and letters in value
    elif len(parsed_data) > 2 or len([char for char in variable_value if char.isdigit()]) > 0 \
            and len([char for char in variable_value if char.isalpha()]) > 0:
        raise TypeError
    # return error if unknown variable to take value from
    elif not variable_value.isdigit():
        raise ValueError
    else:
        return [variable_name, variable_value]


# create equation with numbers instead of variables
def create_equation(indata, variables):
    indata = indata.replace(' ', '')
    parsed_data = list()

    signs = ['(', ')', '*', '/', '-', '+']
    variable = ''
    sign = ''
    previous_char = ''
    x = 0

    if indata[0] in signs[4:]:
        indata = '0' + indata

    #parse indata to create equation
    for char in indata:
        if char in signs[:4]:
            if variable != '':
                parsed_data.append(variable)
                variable = ''
            if sign != '':
                parsed_data.append(sign)
                sign = ''
            parsed_data.append(char)
        elif char in signs[4:] and previous_char not in signs[:4]:
            sign += char
            if variable != '':
                parsed_data.append(variable)
                variable = ''
            if x == len(indata) - 1:
                parsed_data.append(sign)
        else:
            variable += char
            if sign != '':
                parsed_data.append(sign)
                sign = ''
            if x == len(indata) - 1:
                parsed_data.append(variable)
        previous_char = char
        x += 1

    # transform signs from input to final signs
    x = 0
    while x < len(parsed_data):
        plus_qty = parsed_data[x].count('+')
        minus_qty = parsed_data[x].count('-')
        length = len(parsed_data[x])
        if plus_qty + minus_qty == length:  # filter out negative numbers
            if minus_qty == 0 or minus_qty % 2 == 0:
                parsed_data[x] = '+'
            else:
                parsed_data[x] = '-'
        x += 1

    # replace variables with values
    for element in parsed_data:
        if element in variables.keys():
            parsed_data[parsed_data.index(element)] = variables[element]

    return parsed_data


# transform equation from infix notation to prefix notation
def transform_to_prefix(infix_equation):
    infix_equation.reverse()  # reverse equation
    prefix_equation = list()
    stack = list()
    signs = ['*', '/', '-', '+']

    for element in infix_equation:
        if element not in signs and element not in ('(', ')'):
            prefix_equation.append(element)
        elif element == ')':
            stack.append(element)
        elif element == '(':
            while stack[-1] != ')':
                if stack[-1] in signs:
                    prefix_equation.append(stack.pop())
            stack.pop()
        elif element in signs:
            while True:
                if element in signs[2:] and stack != [] and stack[-1] in signs[:2]:
                    prefix_equation.append(stack.pop())
                else:
                    break
            stack.append(element)

    while stack:
        prefix_equation.append(stack.pop())

    prefix_equation.reverse()

    return prefix_equation


def calculate_prefix_equation(prefix_equation):
    result_stack = list()
    operators = {'*': operator.mul, '/': operator.truediv, '+': operator.add, '-': operator.sub}
    operators_stack = list(set(prefix_equation) & set(operators))

    while prefix_equation:
        if prefix_equation[-1] not in operators:
            result_stack.append(int(prefix_equation.pop()))
        elif prefix_equation[-1] in operators:
            a = result_stack.pop()
            b = result_stack.pop()
            result = int(operators[prefix_equation.pop()](a, b))
            result_stack.append(result)

    if operators_stack == [] and len(result_stack) > 1:
        raise ValueError
    else:
        return result_stack.pop()


indata = ''
commands_list = {'/exit': 'Bye!', '/help': 'The program calculates the sum and subtraction of numbers'}
variables = {}
signs = ['*', '/', '-', '+']

while indata != '/exit':
    indata = input('')
    if indata != '' and indata[0] == '/':
        try:
            print(commands_list[indata])
        except Exception:
            print('Unknown command')
    elif '=' in indata:
        try:
            variable = define_variable(indata, variables)
            variables.update({variable[0]: variable[1]})
        except NameError:
            print('Invalid identifier')
        except TypeError:
            print('Invalid assignment')
        except ValueError:
            print('Unknown variable')
    elif any(sign in indata for sign in signs):
        try:
            equation = create_equation(indata, variables)
            prefix_equation = transform_to_prefix(equation)
            result = calculate_prefix_equation(prefix_equation)
            print(result)
        except Exception:
            print('Invalid expression')
            continue
    else:
        try:
            print(return_value(indata, variables))
        except NameError:
            print('Unknown variable')
        except TypeError:
            print('Invalid identifier')
        except ValueError:
            continue
