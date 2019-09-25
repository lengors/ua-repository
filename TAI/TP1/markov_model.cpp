// this file contains the implementation of the MarkovModel class
#include "markov_model.hpp"

#include <iostream>
#include <string>

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
    this->total=0;
	bool exist = false;
    for(int i = 0; i < this->content.length()-k; i++){
		exist = false;
        this->total++;
        charData temp;
        temp.text = "";
        temp.count = 0;
        temp.total = 0;
        for(int j = 0; j<this->k; j++){
            temp.text += this->content[i+j];
            
        }
        temp.c = this->content[i + k ];
        for (charData &str : this->data){
            if(str.text == temp.text && temp.c == str.c){
                
				exist = true;
                str.count++;
                str.total ++;
                break;
            }else if(str.text == temp.text && temp.c != str.c){
                temp.total = str.total;
            }
        }
        
        if(!exist){
            temp.total++;
            temp.count = 1;
            data.push_back(temp);
        }
        this->charTotals[temp.text]++;
        
        //
        
    }
     std::cout << " char appearances " << std::endl;
    for(auto &str : this->data){
       //std::cout << "Text" << " - " << "Char" <<  " - " << "N" << " - " << "T" << std::endl;
        std::cout << str.text << " - " << str.c <<  " - " << str.count  << std::endl;
    }

     std::cout << " Text total appearances " << std::endl;
     for (auto it=charTotals.begin(); it!=charTotals.end(); ++it){
        std::cout << it->first << " => " << it->second << '\n';
     }
      std::cout << " Conditional Probability " << std::endl;
    for(auto &str : data){
        std::cout << "P("<< str.c << "|" << str.text << ") = "<< "(" << str.count << "+" << alpha << ") / (" << charTotals[str.text] 
        << "+" << alpha << "*" << "2 \"size of alphabet\" ) = " << ((float)str.count + alpha) / ((alpha*2) + charTotals[str.text]) << std::endl;
    }
    
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

    for (auto& str : data){
        tempfile << str.text << " - " << str.c << " - " << str.count << "\n";
    }
   


}


