from lark import Lark, Token, Transformer
from lark.tree import Tree
from lark.tree_matcher import TreeMatcher
from lark.reconstruct import WriteTokensTransformer


GRAMMAR = """
	?start: sum
	?sum: product
		| sum "+" product   -> add
		| sum "-" product   -> sub
	?product: atom
		| product "*" atom  -> mul
		| product "/" atom  -> div
		| product "^" atom  -> exp
	?atom: "-" atom         -> neg
		 | CONSTANT         -> number
		 | NAME             -> var
		 | "'" QUOTED "'"     -> literal
		 | "\\"" QUOTED "\\"" -> literal
		 | "‘" QUOTED "’"     -> literal
		 | "“" QUOTED "”"     -> literal
		 | "(" sum ")"
	%import common.LETTER
	%import common.DIGIT
	%import common.NUMBER
	%import common.WS_INLINE
	%ignore WS_INLINE

	CONSTANT: DIGIT ("." DIGIT+)?
	NAME: /([^\+\-\*\/\^\(\)\'\"\‘\’\“\”]+|[a-zA-Z]+)/
	QUOTED: /([^\+\-\*\/\^\(\)\'\"\‘\’\“\”]+|[a-zA-Z]+)/
"""

larkParser = Lark(GRAMMAR, parser='lalr')
Ticker = larkParser.parse

class TickerTree(Transformer):
	def add(self, tree): return self.genenrate_list(tree, "add")
	def sub(self, tree): return self.genenrate_list(tree, "sub")
	def mul(self, tree): return self.genenrate_list(tree, "mul")
	def div(self, tree): return self.genenrate_list(tree, "div")
	def exp(self, tree): return self.genenrate_list(tree, "exp")
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

class Reconstructor(TreeMatcher):
	write_tokens: WriteTokensTransformer

	def __init__(self):
		TreeMatcher.__init__(self, larkParser)
		self.write_tokens = WriteTokensTransformer({t.name:t for t in self.tokens}, {})

	def _reconstruct(self, tree):
		unreduced_tree = self.match_tree(tree, tree.data)

		res = self.write_tokens.transform(unreduced_tree)
		for item in res:
			if isinstance(item, Tree):
				yield from self._reconstruct(item)
			elif hasattr(item, "value"):
				yield item.value["id"]
			else:
				yield item

	def reconstruct(self, tree):
		x = self._reconstruct(tree)
		y = []
		for item in x:
			y.append(item)
		return ''.join(y)

reconstructor = Reconstructor()