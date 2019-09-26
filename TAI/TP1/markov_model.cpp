// this file contains the implementation of the MarkovModel class
#include "markov_model.hpp"

#include <iostream>
#include <string>
#include <math.h>

// using namespace std; <- not recommended, may create ambiguity

// constructor



MarkovModel::MarkovModel (const unsigned &k, const unsigned &alpha) :
    k(k), alpha(alpha)
{
    
}

// destructor
MarkovModel::~MarkovModel (void)
{
}

// reads file and builds model
MarkovModel &operator>> (std::ifstream &fileStream, MarkovModel &model)
{
    char letter;
    // iterates over every character in the file
    // and counts how many times each character appears
    // TODO: replace with (k) sequence of characters
    
    
    
    
    while (fileStream.get(letter))
    {   
        
        std::unordered_map<char, unsigned>::iterator iterator = model.frequency.find(letter);
        if (iterator == model.frequency.end())
            model.frequency[letter] = 1;
        else
            ++iterator->second; // slightly more efficient than "++frequency[letter]"";
    
        model.content += letter;
    }    
    std::cout << model.content << std::endl;
    return model;
}

void MarkovModel::analyze(){
    
	bool exist = false;
    for(int i = 0; i < this->content.length()-k; i++){
		exist = false;
       
        CharData temp;
        std::string text = "";
        temp.count = 0;
     
        for(int j = 0; j<this->k; j++){
            text += this->content[i+j];
            
        }
        temp.c = this->content[i + k ];
        for(auto &obj : tableMap[text]){
            if(obj.c == temp.c){
                obj.count++;
                exist = true;
                break;
            }
        }
        if(!exist){
<<<<<<< HEAD
            temp.count = 1;
            data.push_back(temp);
        }  
        
    }   
=======
            temp.count=1;
            tableMap[text].push_back(temp);
        }
        
        
    }
     
   
     std::cout << " Text total appearances " << std::endl;
     for (auto it=tableMap.begin(); it!=tableMap.end(); ++it){
        std::cout << it->first << "-";
        for(auto &symbol : tableMap[it->first]){
            std::cout <<"[" <<symbol.c <<"," << symbol.count<<"]"<<", ";
        }
        std::cout << ";\n";
     }
      std::cout << " Conditional Probability " << std::endl;

    for (auto it=tableMap.begin(); it!=tableMap.end(); ++it){
        for(auto &obj : tableMap[it->first]){
            int count = 0;
            for (auto &obj2 : tableMap[it->first])
                count+= obj2.count;
            std::cout << it->first << " followed by " << obj.c << ":" << ((float)obj.count + alpha) / ((alpha*frequency.size()) + count) << std::endl;
        }
    }


   
>>>>>>> e2ce5aed013d30fde7318030cc83383768357df8
    
}

void MarkovModel::writeToFile(std::string filename){
    std::ofstream tempfile;
    tempfile.open("output.txt");
    tempfile << "k = " << k << "\n";
    tempfile << "alpha = " << alpha << "\n";
    tempfile << "\n";
    for (auto& it : frequency){
        tempfile << it.first << " - " << it.second << "\n";
    }
    tempfile << "\n";

    // for (auto& str : data){
    //     tempfile << str.text << " - " << str.c << " - " << str.count << "\n";
    // }
   


}


float MarkovModel::calcEntropy(){
    return log2(frequency.size());
}


