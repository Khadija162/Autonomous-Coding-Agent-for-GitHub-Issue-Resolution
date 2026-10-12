"""Tree-sitter Python syntax verification for proposals."""
from tree_sitter import Language, Parser
import tree_sitter_python

def check_python(text: str):
    tree = Parser(Language(tree_sitter_python.language())).parse(text.encode())
    return {"valid": not tree.root_node.has_error, "root_type": tree.root_node.type}
