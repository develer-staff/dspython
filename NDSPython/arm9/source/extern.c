#include "extern.h"

void decompress_file(char *filename,unsigned int dst,DecompressType type){
        unsigned int size=0,*buffer=NULL;
	FILE *fp=fopen(filename,"rb");
	fread(&size,4,1,fp);
	buffer=(unsigned int*)malloc(size);
	fread(buffer,1,size,fp);
	decompress(buffer, (u16*)dst,  type);
	fclose(fp);
	free(buffer);
}