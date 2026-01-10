import ast
import operator
from collections.abc import Callable
from typing import Final, TypeAlias

import discord
from discord import app_commands
from discord.ext import commands

Number: TypeAlias = int | float

_BinFn: TypeAlias = Callable[[Number, Number], Number]
_IntBinFn: TypeAlias = Callable[[int, int], int]
_UnaryFn: TypeAlias = Callable[[Number], Number]

class _CalcError(Exception):
    pass

_MAX_EXPRESSION_LENGTH: Final[int] = 256
_MAX_NODES: Final[int] = 128

_ARITH_BIN_OPS: Final[dict[type[ast.operator], _BinFn]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_INT_BIN_OPS: Final[dict[type[ast.operator], _IntBinFn]] = {
    ast.BitOr: operator.or_,
    ast.BitXor: operator.xor,
    ast.BitAnd: operator.and_,
    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
}

_NUM_UNARY_OPS: Final[dict[type[ast.unaryop], _UnaryFn]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _require_int(value: Number) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise _CalcError("整数のみが使用できます。")
    return value

def _as_number(value: object) -> Number:
    if isinstance(value, bool):
        raise _CalcError("真偽値は使用できません。")
    if isinstance(value, (int, float)):
        return value
    raise _CalcError("数値のみが使用できます。")

def _eval_expr(node: ast.AST, *, node_budget: list[int]) -> Number:
    node_budget[0] -= 1
    if node_budget[0] < 0:
        raise _CalcError("式が複雑すぎます。")

    if isinstance(node, ast.Constant):
        return _as_number(node.value)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        operand = _eval_expr(node.operand, node_budget=node_budget)

        if op_type is ast.Invert:
            return operator.invert(_require_int(operand))

        fn = _NUM_UNARY_OPS.get(op_type)
        if fn is None:
            raise _CalcError("未対応の単項演算子です。")
        return _as_number(fn(operand))

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        left = _eval_expr(node.left, node_budget=node_budget)
        right = _eval_expr(node.right, node_budget=node_budget)

        int_fn = _INT_BIN_OPS.get(op_type)
        if int_fn is not None:
            return _as_number(int_fn(_require_int(left), _require_int(right)))

        num_fn = _ARITH_BIN_OPS.get(op_type)
        if num_fn is None:
            raise _CalcError("未対応の二項演算子です。")

        if op_type is ast.Pow and isinstance(right, int) and abs(right) > 10_000:
            raise _CalcError("指数が大きすぎます。")

        return _as_number(num_fn(left, right))

    raise _CalcError("許可されていない式です。")

def _calculate(expression: str) -> Number:
    expr = expression.strip()
    if not expr:
        raise _CalcError("式が空です。")
    if len(expr) > _MAX_EXPRESSION_LENGTH:
        raise _CalcError("式が長すぎます。")

    try:
        parsed: ast.Expression = ast.parse(expr, mode="eval")
    except SyntaxError:
        raise _CalcError("式の構文が正しくありません。")

    return _eval_expr(parsed.body, node_budget=[_MAX_NODES])

class CalculatorCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="calculate", description="Pythonの演算子で計算を行います。")
    @app_commands.default_permissions(administrator=True)
    async def calculate(self, interaction: discord.Interaction, expression: str) -> None:
        if not interaction.guild:
            return

        try:
            result = _calculate(expression)
        except _CalcError as e:
            await interaction.response.send_message(str(e), ephemeral=True)
            return
        except Exception:
            await interaction.response.send_message("計算に失敗しました。", ephemeral=True)
            return

        safe_expr = discord.utils.escape_markdown(expression.strip())
        await interaction.response.send_message(f"式: {safe_expr}\n結果: {result}", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CalculatorCommand(bot))

