#include<iostream>
#include<fstream>

using namespace std;


int main(int argc, char * argv[]) {
    
    if (argc < 3){
        cerr << "Número inválido de argumentos!!" << endl;
        return 1;
    }

    int k = stoi(argv[1]);
    int alpha = stoi(argv[2]);

    if (argc == 3)
        string text = "text.txt";

    else
        string text = argv[3];

    return 0;
}