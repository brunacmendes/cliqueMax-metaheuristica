var x1 binary;
var x2 binary;
var x3 binary;
var x4 binary;
var x5 binary;
var x6 binary;

maximize NumNos: x1 + x2 + x3 + x4 + x5 + x6;

subject to 

arco15: x1 + x5 <= 1; 
arco25: x2 + x5 <= 1; 
arco35: x3 + x5 <= 1; 
arco16: x1 + x6 <= 1; 
arco26: x2 + x6 <= 1; 
arco46: x4 + x6 <= 1; 

solve;
display NumNos, x1, x2, x3, x4, x5, x6;