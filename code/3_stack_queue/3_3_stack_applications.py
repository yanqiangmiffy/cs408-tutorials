"""
栈的应用: 括号匹配 + 表达式求值

1. 括号匹配:
   - 遇到左括号入栈
   - 遇到右括号与栈顶匹配
   - 最终栈空则匹配成功

2. 中缀表达式转后缀 + 后缀表达式求值:
   - 中缀: 3 + 4 * 2
   - 后缀: 3 4 2 * +
   - 前缀: + 3 * 4 2
"""


def bracket_matching(expr):
    """括号匹配算法

    思路:
    1. 扫描表达式
    2. 遇到左括号 → 入栈
    3. 遇到右括号 → 检查栈顶是否匹配
    4. 扫描完毕, 栈空则匹配成功
    """
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}

    for i, ch in enumerate(expr):
        if ch in pairs:  # 左括号
            stack.append(ch)
        elif ch in pairs.values():  # 右括号
            if not stack:
                return False, f"位置{i}: 右括号'{ch}'多余"
            top = stack.pop()
            if pairs[top] != ch:
                return False, f"位置{i}: '{top}'与'{ch}'不匹配"

    if stack:
        return False, f"左括号多余: {stack}"
    return True, "匹配成功"


def infix_to_postfix(expr):
    """中缀表达式转后缀表达式 (逆波兰式)

    规则:
    1. 操作数直接输出
    2. 左括号入栈
    3. 右括号: 弹出直到遇到左括号
    4. 运算符: 弹出栈中优先级 >= 当前运算符的，再入栈
    5. 扫描完毕，栈中剩余全部弹出

    优先级: * / > + -
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = []
    output = []
    tokens = tokenize(expr)

    print(f"  中缀表达式: {expr}")
    print(f"  {'token':>8s} {'动作':>12s} {'栈':>15s} {'输出':>20s}")
    print(f"  {'─' * 60}")

    for token in tokens:
        if token.replace('.', '').isdigit():  # 操作数
            output.append(token)
            action = "输出"
        elif token == '(':
            stack.append(token)
            action = "入栈"
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # 弹出 '('
            action = "弹至("
        elif token in precedence:
            while (stack and stack[-1] != '(' and
                   stack[-1] in precedence and
                   precedence[stack[-1]] >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)
            action = "比较入栈"
        print(f"  {token:>8s} {action:>12s} {str(stack):>15s} {' '.join(output):>20s}")

    while stack:
        output.append(stack.pop())

    print(f"  {'清栈':>8s} {'弹出':>12s} {str(stack):>15s} {' '.join(output):>20s}")
    return output


def evaluate_postfix(postfix):
    """后缀表达式求值

    规则:
    1. 遇到操作数 → 入栈
    2. 遇到运算符 → 弹出两个操作数，计算后入栈
    3. 最后栈中唯一元素即为结果

    注意: 先弹出的是右操作数!
    """
    stack = []
    print(f"\n  后缀表达式求值: {' '.join(postfix)}")
    print(f"  {'token':>8s} {'动作':>20s} {'栈':>20s}")
    print(f"  {'─' * 50}")

    for token in postfix:
        if token.replace('.', '').isdigit():
            stack.append(float(token))
            print(f"  {token:>8s} {'入栈':>20s} {str(stack):>20s}")
        else:
            b = stack.pop()  # 右操作数
            a = stack.pop()  # 左操作数
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                result = a / b
            stack.append(result)
            desc = f"{a}{token}{b}={result}"
            print(f"  {token:>8s} {desc:>20s} {str(stack):>20s}")

    return stack[0]


def tokenize(expr):
    """将表达式字符串分割为 token 列表"""
    tokens = []
    i = 0
    expr = expr.replace(' ', '')
    while i < len(expr):
        if expr[i].isdigit() or expr[i] == '.':
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
        else:
            tokens.append(expr[i])
            i += 1
    return tokens


def bracket_demo():
    """括号匹配演示"""
    print("=" * 60)
    print("括号匹配")
    print("=" * 60)

    test_cases = [
        "(())",
        "({[]})",
        "(()",
        "([)]",
        "{[()]}",
        "",
        ")()",
    ]

    for expr in test_cases:
        ok, msg = bracket_matching(expr)
        mark = "✓" if ok else "✗"
        display = expr if expr else "(空串)"
        print(f"  {mark} {display:15s} → {msg}")
    print()


def expression_demo():
    """表达式求值演示"""
    print("=" * 60)
    print("中缀转后缀 + 后缀求值")
    print("=" * 60)

    expressions = [
        "3 + 4 * 2",
        "(3 + 4) * 2",
        "2 * (3 + 4) - 5",
    ]

    for expr in expressions:
        print(f"\n{'─' * 60}")
        postfix = infix_to_postfix(expr)
        result = evaluate_postfix(postfix)
        print(f"\n  后缀: {' '.join(postfix)}")
        print(f"  结果: {result}")
    print()


if __name__ == "__main__":
    bracket_demo()
    expression_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 括号匹配:
     左括号入栈，右括号与栈顶匹配
     匹配失败的三种情况:
     ① 右括号多余 (栈空遇到右括号)
     ② 左括号多余 (扫描完栈非空)
     ③ 括号不匹配 (栈顶与当前不配对)

  2. 中缀转后缀:
     操作数直接输出
     运算符与栈顶比较优先级
     优先级高或等于 → 栈顶弹出输出

  3. 后缀表达式求值:
     操作数入栈，运算符弹两个计算
     先弹出的是右操作数!

  4. 三种表达式:
     中缀: A + B * C     (需要括号和优先级)
     后缀: A B C * +     (无需括号, 从左到右扫描)
     前缀: + A * B C     (无需括号, 从右到左扫描)
    """)
