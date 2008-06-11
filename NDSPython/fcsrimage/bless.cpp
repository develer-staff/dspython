#include <stdlib.h>
#include <stdio.h>
#include "gba_types.h"


int main( int argc, char *argv[])
{
    FILE *fp;
    if(argc < 2) {
        printf("Usage: %s diskimage.fat [overlay start sector]\n", argv[0]);
        return 1;
    }

    fp = fopen(argv[1], "r+");
    if(!fp) {
        perror("opening disk image");
        return 1;
    }

    fseek(fp, 0x100, SEEK_SET);

    char *magic = "FCSR Chishm FAT\0";
    int wrote = fwrite(magic, 1, 16, fp);
    if(wrote != 16) {
        perror("writing magic");
        fclose(fp);
        return 1;
    }

    s32 start1 = -1;
    if(argc > 2)
        start1 = atoi(argv[2]);
        
    u32 size1 = 120;
    if(argc <= 2 || atoi(argv[2]) < 0)
    {
        start1 = 0;
        size1 = 0;
    }
    u32 zero = 0;

    wrote = fwrite(&start1, 1, 4, fp);
    wrote += fwrite(&zero, 1, 4, fp);
    wrote += fwrite(&zero, 1, 4, fp);
    wrote += fwrite(&zero, 1, 4, fp);
    wrote += fwrite(&size1, 1, 4, fp);
    wrote += fwrite(&zero, 1, 4, fp);
    wrote += fwrite(&zero, 1, 4, fp);
    wrote += fwrite(&zero, 1, 4, fp);

    fclose(fp);

    if(wrote != 4*8) {
       perror("writing sram overlay");
       return 1;
    } 

    printf("OK - start1:%d size1:%d\n", start1, size1);

    return 0;
}
