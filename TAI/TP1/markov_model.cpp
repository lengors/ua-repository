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
        for(int j = 0; j<this->k; j++){
            temp.text += this->content[i+j];
            
        }
        temp.c = this->content[i + k ];
        for (charData &str : this->data){
            if(str.text == temp.text && temp.c == str.c){
                
				exist = true;
                str.count++;
                break;
            }
        }
        
        if(!exist){
            temp.count = 1;
            data.push_back(temp);
        }
        
        
        //
        
    }
    for(auto &str : this->data){
        std::cout << str.text << " - " << str.c <<  " - " << (float(str.count) / float(this->total)) << std::endl;
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


