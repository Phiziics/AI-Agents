import ast
import operator
import re
from typing import Union

from crewai.tools import BaseTool


class CalculatorTool(BaseTool):
    name: str = "Make a calculation"
    description: str = (
        "Perform safe mathematical calculations like 200*7, 5000/2*10, "
        "or (100 + 50) / 3. Only basic numeric operations are allowed."
    )

    def _run(self, operation: str) -> str:
        """
        Safely evaluate a basic mathematical expression and return the result as a string.
        """
        try:
            allowed_operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.Mod: operator.mod,
                ast.USub: operator.neg,
                ast.UAdd: operator.pos,
            }

            if not re.match(r"^[0-9+\-*/().% ]+$", operation):
                return "Error: Invalid characters in mathematical expression."

            tree = ast.parse(operation, mode="eval")

            def _eval_node(node: ast.AST) -> Union[int, float]:
                if isinstance(node, ast.Expression):
                    return _eval_node(node.body)
                elif isinstance(node, ast.Constant):
                    if isinstance(node.value, (int, float)):
                        return node.value
                    raise TypeError("Only numeric constants are allowed.")
                elif isinstance(node, ast.Num):
                    return node.n
                elif isinstance(node, ast.BinOp):
                    left = _eval_node(node.left)
                    right = _eval_node(node.right)
                    op = allowed_operators.get(type(node.op))
                    if op is None:
                        raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
                    return op(left, right)
                elif isinstance(node, ast.UnaryOp):
                    operand = _eval_node(node.operand)
                    op = allowed_operators.get(type(node.op))
                    if op is None:
                        raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
                    return op(operand)
                else:
                    raise ValueError(f"Unsupported node type: {type(node).__name__}")

            result = _eval_node(tree)
            return str(result)

        except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as e:
            return f"Error: {str(e)}"
        except Exception:
            return "Error: Invalid mathematical expression."
