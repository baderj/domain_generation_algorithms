#include <stdio.h>
#include <stdlib.h>

char* dga(unsigned int day, unsigned int month, unsigned int year, 
        unsigned int seed, unsigned int nr) 
{
    char *tlds[] = {"in", "me", "cc", "su", "tw", "net", "com", "pw", "org"};
    char domain[15];
    int d;
    int tld_index = day;
    for(d = 0; d < nr; d++)
    {
        unsigned int i;
        for(i = 0; i < 14; i++)
        {
            day = (day >> 15) ^ 16 * (day & 0x1FFF ^ 4 * (seed ^ day));
            year = ((year & 0xFFFFFFF0) << 17) ^ ((year ^ (7 * year)) >> 11);
            month = 14 * (month & 0xFFFFFFFE) ^ ((month ^ (4 * month)) >> 8);
            seed = (seed >> 6) ^ ((day + 8 * seed) << 8) & 0x3FFFF00;
            int x = ((day ^ month ^ year) % 25) + 97; 
            domain[i] = x;
        }
        printf("%s.%s\n", domain, tlds[tld_index++ % 8]);
    }
}

int main (int argc, char *argv[])
{
    if(argc != 5) {
        printf("Usage: dga <day> <month> <year> <seed>\n");
        printf("Example: dga 14 5 2015 b6354bc3\n"); 
        exit(0);
    }
    /* known seeds:
            C5F128F3 
            B6354BC3 
            65BA0743 
            0478620C 
    */

    dga(atoi(argv[1]), atoi(argv[2]), atoi(argv[3]), 
            strtoul(argv[4], NULL, 16), 40);
}
