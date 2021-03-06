%module VD1
%include cpointer.i
%include "std_vector.i"
%pointer_functions(int, intp);
namespace std{
	%template(vectori) vector<int>;
	%template(vectorb) vector<bool>;
	%template(vectorf1) vector<float>;
	%template(vectorf2) vector<vector<float>>;
	%template(vectorf3) vector<vector<vector<float>>>;
};
%{
#include "VD1.h"
%}
%include VD1.h