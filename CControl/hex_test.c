/*
 *
 * Q: can we write unsigned chars with decimal?
 *
 * Yes, initializing with 80 vs. initializing with 0x50 gives us same thing
 *
 */
#include <stdio.h>
#include <stdlib.h>



int main(){

    // decimal:
    unsigned char a = 80;
    // hex:
    unsigned char b = 0x50; 

    int size_i = sizeof(a); 

    printf("%u\n", a); 
    printf("%u\n", b); 
    printf("%d\n", size_i);

    // testing sizeof:
    int ar[2] = {1,2};
    size_i = sizeof(ar);
    printf("%d\n", size_i); 

}
