 
##`main.py` 

from lexer         import tokenize, print_tokens
from parser        import Parser,   print_tree
from semantic      import SemanticAnalyzer
from ai_correction import run_ai_correction

# ─────────────────────────────────────────────────────
#  C++ SOURCE CODE WITH INTENTIONAL ERRORS IN ALL PHASES
#
#  Lexical  error  : @ symbol (unknown character) on line 7
#  Syntax   error  : missing semicolon after 'result' declaration
#  Semantic error  : int variable assigned a string literal
#                    + undeclared variable 'undefined_var' used
# ─────────────────────────────────────────────────────
SOURCE_CODE = """\
#include <iostream>
using namespace std;

int main() {
    intt x = 10;
    int y = 20;
    int z = x + y;
    num = "hello";
    float result = x + y
    int val = @;
    cout << z << endl;
    cout << undefined_var << endl;
    return 0;
}
"""
# ─────────────────────────────────────────────────────

def main():
    print("\n" + "="*60)
    print("  COMPILER WITH INTERACTIVE AI CORRECTION")
    print("="*60)
    
    print("\n  Source code under analysis:")
    print("  " + "-"*50)
    for i, line in enumerate(SOURCE_CODE.strip().splitlines(), 1):
        print(f"  {i:>3} | {line}")
    print("  " + "-"*50)

    # Phase 1 — Lexical
    tokens, lex_errors = tokenize(SOURCE_CODE)
    print_tokens(tokens, lex_errors)

    # Phase 2 — Syntax
    parser     = Parser(tokens)
    tree       = parser.parse()
    syn_errors = parser.errors
    print_tree(tree, syn_errors)

    # Phase 3 — Semantic
    analyzer   = SemanticAnalyzer(tree)
    analyzer.analyze()
    analyzer.print_results()
    sem_errors = analyzer.errors

    # Interactive 3-Phase AI Correction
    run_ai_correction(SOURCE_CODE, lex_errors, syn_errors, sem_errors)

if __name__ == "__main__":
    main()