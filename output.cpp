#include <iostream> 
using namespace std; 
int main() { 
int e = 111;
cout << e << endl;
int x = e;
cout << e << " " << x << endl;
cin >> e >> x;
cout << e << " " << x << endl;
if (true) {
int z = 111;
cout << z << endl;
}
return 0;
}