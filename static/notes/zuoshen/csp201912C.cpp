#include <bits/stdc++.h>
using namespace std;
struct ele_set{
    unordered_map<string, int> ump;
    bool operator==(const ele_set & other) const{
        return ump == other.ump;
    }
    void operator+=(const ele_set & other){
        for (auto & [k, v] : other.ump){
            ump[k] += v;
        }
    }
    void operator*=(const int v){
        for (auto & [k, v0] : ump){
            v0 *= v;
        }
    }
};
vector<string> split(string & s, char c){
    vector<string> ans;
    stringstream ss(s);
    string cur;
    while (getline(ss, cur, c)){
        ans.push_back(cur);
    }
    return ans;
}
string r_el(string & s, int & p){
    string res;
    res += s[p++];
    if (p < s.size() && islower(s[p])){
        res += s[p++];
    }
    return res;

}
int r_int(string & s, int & p){
    int res = 0;
    while (p < s.size() && isdigit(s[p])){
        res = res * 10 + (s[p] - '0');
        p++;
    }
    if (res == 0) res = 1;
    return res;
}
ele_set str2set(string & s, int & p){
    ele_set res;
    int multi = r_int(s, p);
    while (p < s.size()){
        if (s[p] == '('){
            p++;
            res += str2set(s, p);
        }
        else if(s[p] == ')'){
            p++;
            res *= r_int(s, p);
            break;
        }
        else{
            string el = r_el(s, p);
            res.ump[el] += r_int(s, p);
        }
    }
    res *= multi;
    return res;
}
bool solve(string & s){
    vector<string> fms = split(s, '=');
    ele_set res[2];
    for(int i = 0; i<2;i++){
        vector<string> terms = split(fms[i], '+');
        for (auto & term : terms){
            int p = 0;
            res[i] += str2set(term, p);
        }
    }
    return res[0] == res[1];
}
int main(){
    int n;
    cin >> n;
    while (n--){
        string s;
        cin >> s;
        if (solve(s)){
            cout << "Y\n";
        }
        else{
            cout << "N\n";
        }
    }
}
