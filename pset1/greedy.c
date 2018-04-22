#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    int change;
    int counter = 0;
    int balance;
    
    printf("O hai! ");
    do
    {
        printf("How much change is owed?\n");
        dollars = get_float();
    } while (dollars < 0);
    
    balance = round(dollars * 100);
    
    // quarters
    change = balance % 25;
    counter += (balance - change)/25;

    // dimes
    balance = change;
    change = balance % 10;
    counter += (balance - change)/10;

    // nickels
    balance = change;
    change = change % 5;
    counter += (balance - change)/5;

    // pennies
    balance = change;
    change = balance % 1;
    counter += (balance - change)/1;
    
    printf("%i\n", counter); 
}