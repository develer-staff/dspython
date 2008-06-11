#include <stdlib.h>
#include <stdio.h>
#include "gba_types.h"


int main( int argc, char *argv[])
{
    FILE *fp;
    if(argc < 3) {
        printf("Error! Usage: %s [diskimage.fat] [size in KB]\n", argv[0]);
        return 1;
    }

    fp = fopen(argv[1], "w");
    if(!fp) {
        perror("opening disk image for write");
        return 1;
    }

    int size = atoi(argv[2])*1024;

    u8 *zero = (u8 *)malloc(size);
    for(int i=0; i<size; i++)
        zero[i] = 0;

    int wrote = fwrite(zero, 1, size, fp);
    fclose(fp);
    if(wrote != size)
    {
        perror("creating full image");
        return 1;
    }

    printf("OK\n");

    return 0;
}
