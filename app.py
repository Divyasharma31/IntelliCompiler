from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from lexer import tokenize
from parser import Parser, format_node
from semantic import SemanticAnalyzer
from ai_correction import get_ai_fix
import os

app = Flask(__name__, static_folder='static')
CORS(app) # Enable CORS just in case

# Example code from main.py
EXAMPLE_CODE = """#include <iostream>
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

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/example', methods=['GET'])
def get_example():
    return jsonify({'code': EXAMPLE_CODE})

@app.route('/run_phase', methods=['POST'])
def run_phase():
    data = request.json
    code = data.get('code', '')
    phase = data.get('phase', '')
    
    if phase == 'lexical':
        tokens, errors = tokenize(code)
        return jsonify({
            'tokens': [{'type': t[0], 'value': t[1], 'line': t[2]} for t in tokens],
            'errors': errors
        })
    
    elif phase == 'syntax':
        tokens, _ = tokenize(code)
        parser = Parser(tokens)
        tree = parser.parse()
        formatted_tree = [format_node(node) for node in tree]
        return jsonify({
            'tree': formatted_tree,
            'errors': parser.errors
        })
        
    elif phase == 'semantic':
        tokens, _ = tokenize(code)
        parser = Parser(tokens)
        tree = parser.parse()
        analyzer = SemanticAnalyzer(tree)
        analyzer.analyze()
        
        symbol_table = []
        for name, typ in analyzer.symbols.items():
            symbol_table.append({'name': name, 'type': typ})
            
        return jsonify({
            'symbol_table': symbol_table,
            'warnings': analyzer.warnings,
            'errors': analyzer.errors
        })
    
    return jsonify({'error': 'Invalid phase'}), 400

@app.route('/ai_correct', methods=['POST'])
def ai_correct():
    data = request.json
    code = data.get('code', '')
    errors = data.get('errors', [])
    phase = data.get('phase', '')
    
    result = get_ai_fix(phase, code, errors)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
