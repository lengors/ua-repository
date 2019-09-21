
#include<iostream>
#include<fstream>
#include <map>

using namespace std;

class ReadFile {

    private : 

        string filename;
        int k;
        int alpha;
        map<char, int> frequency;   // frequência absoluta das letras
        
    public : 
        

        ReadFile(string file, int num1, int num2) {
            filename = file;
            k = num1;
            alpha = num2;
        }

        void read() {
            char letter;
            ifstream reader(filename);

            if (!reader) {
                cout << "Error opening the file!!" << endl;
                return;
            }

            for (int i = 0; ! reader.eof(); i++){
                reader.get(letter);
                if (frequency.find(letter) != frequency.end() ){
                    frequency[letter]++;
                } else{
                    frequency[letter] = 1;
                }
              
                
            }


            reader.close();
        }

        map<char, int> getFrequency() {
            return frequency;
        }

};


int main() {

    ReadFile rf("text.txt", 1, 1);

    rf.read();

    for(auto elem : rf.getFrequency())
        {
           cout << elem.first << " " << elem.second << "\n";
        }

    return 0;
}