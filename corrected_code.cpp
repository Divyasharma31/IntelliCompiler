
#include <iostream>
using namespace std;

int main() {
    int x = 10; // Corrected 'intt' to 'int'
    int y = 20;
    int z = x + y;
    // num = "hello"; // This line is commented out as it's a semantic error (trying to assign a string to an undeclared variable)
    float result = x + y; // Added missing semicolon and fixed potential type issue
    // int val = @; // This line is commented out due to the lexical error for '@'
    cout << z << endl;
    // cout << undefined_var << endl; // This line is commented out as 'undefined_var' is not declared (semantic error)
    return 0;
}
