from lark import Lark, Token, Transformer
from lark.reconstruct import Reconstructor

GRAMMAR = """
	?start: sum
	?sum: product
		| sum "+" product   -> add
		| sum "-" product   -> sub
	?product: atom
		| product "*" atom  -> mul
		| product "/" atom  -> div
	?atom: "-" atom         -> neg
		 | CONSTANT         -> number
		 | NAME             -> var
		 | NAME ":" NUMBER  -> var
		 | "'" NAME "'"     -> literal
		 | "\\"" NAME "\\"" -> literal
		 | "‘" NAME "’"     -> literal
		 | "“" NAME "”"     -> literal
		 | "(" sum ")"
	%import common.LETTER
	%import common.DIGIT
	%import common.NUMBER
	%import common.WS_INLINE
	%ignore WS_INLINE

	NAME: DIGIT* LETTER ("_"|":"|"!"|LETTER|DIGIT)*
	CONSTANT: DIGIT ("." DIGIT+)?
"""

larkParser = Lark(GRAMMAR, parser='lalr')
Ticker = larkParser.parse
Reconstructor = Reconstructor(larkParser)

class TickerTree(Transformer):
	def add(self, tree): return self.genenrate_list(tree, "add")
	def sub(self, tree): return self.genenrate_list(tree, "sub")
	def mul(self, tree): return self.genenrate_list(tree, "mul")
	def div(self, tree): return self.genenrate_list(tree, "div")
	def neg(self, tree): return self.genenrate_list(tree, "neg")
	def var(self, tree): return self.genenrate_list(tree, "var")
	def number(self, tree): return self.genenrate_list(tree, "number")
	def name(self, tree): return self.genenrate_list(tree, "name")
	def literal(self, tree): return self.genenrate_list(tree, "literal")

	def genenrate_list(self, tree, method):
		l = [method, []]
		for child in tree:
			if not isinstance(child, Token): l[1].append(child)
			else: l[1].append([child.type, child.value])
		return l