#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;
string getTypeName(int tokenType){
  switch (tokenType) {
    case 0:
      return "int       ";
    case 1:
      return "word      ";
    case 2:
      return "equals    ";
    case 3:
      return "keyword   ";
  }
  return "unk ";
}
int main(){
  ifstream source;
  source.open("source.txt");
  if (!source) {
    cout << "file not found or not readable";
    exit(1);
  }
  char c;
  vector<string> tokenStrings;
  vector<int> tokenTypes;
  // -1 = BEGIN
  // 0 = int
  // 1 = name
  // 2 = equals
  // 3 = type
  // 4 = equ
  int lastType = -1;
  string currentToken;
  string specials[3] = {"int","str","bool"};
  while (source.get(c)) {
    int asciiId = (int) c;
    if (asciiId <= 57 && asciiId >= 48 && lastType != 1){
      if (lastType == 0){
        currentToken += (string) &c;
      }
      else{
        tokenStrings.insert(tokenStrings.begin(),currentToken);
        tokenTypes.insert(tokenTypes.begin(),0);
        currentToken = (string) &c;
      }
      lastType = 0;
    }
    else if (c == ' '){
      lastType = -1;
    }
    else if (c == '\n'){
      lastType = -1;
    }
    else{
      if (lastType == 1){
        currentToken += (string) &c;
      }
      else{
        tokenStrings.insert(tokenStrings.begin(),currentToken);
        int tokenTypeStr;
        if (currentToken == "int" || currentToken == "str"){/// || currentToken != "str"){
          tokenTypeStr = 3;
        }
        else {
          tokenTypeStr = 1;
        };
        //cout << specials[i] << " " << currentToken <<( specials[i] == currentToken) << endl;
        //cout << tokenTypeStr << endl;
        //cout << tokenTypeStr << endl;
        tokenTypes.insert(tokenTypes.begin(),tokenTypeStr);
        currentToken = (string) &c;
      }
      lastType = 1;
    }

  }
  tokenStrings.insert(tokenStrings.begin(),currentToken);
  for (int tokenPlace = tokenStrings.size()-2; tokenPlace >= 0; tokenPlace --){
    //int curType = tokenTypes[tokenPlace];
    string token = tokenStrings[tokenPlace];
    cout << getTypeName(tokenTypes[tokenPlace]);
    cout << token;
    cout << endl;
  }
}
