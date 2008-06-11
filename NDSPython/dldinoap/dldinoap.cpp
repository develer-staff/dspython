#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void print_header()
{
    fprintf(stdout,"=== DLDI no-autopatch by PsychoWood ===\n");
}

static void print_usage()
{
    fprintf(stdout,"USAGE   :  dldinoap ROMFILE\n");
    fprintf(stdout,"\n"); 
}

static bool parse_command(int argc, char** argv)
{
    if(argc != 2) 
		return false;
	else
		return true;
}

unsigned long FileSearch(FILE* pFile, const char* lpszSearchString)
{
	// Credits goes to Sean Eshbaugh
	// http://www.geekpedia.com/tutorial38_Searching-for-a-string-in-a-File.html

    //make sure we were passed a valid, if it isn't return -1
    if ((!pFile)||(!lpszSearchString))
    {
        return -1;
    }

    unsigned long ulFileSize=0;

    //get the size of the file
    fseek(pFile,0,SEEK_END);

    ulFileSize=ftell(pFile);

    fseek(pFile,0,SEEK_SET);

    //if the file is empty return -1
    if (!ulFileSize)
    {
        return -1;
    }

    //get the length of the string we're looking for, this is
    //the size the buffer will need to be
    unsigned long ulBufferSize=strlen(lpszSearchString);

    if (ulBufferSize>ulFileSize)
    {
        return -1;
    }

    //allocate the memory for the buffer
    char* lpBuffer=(char*)malloc(ulBufferSize);

    //if malloc() returned a null pointer (which probably means
    //there is not enough memory) then return -1
    if (!lpBuffer)
    {
        return -1;
    }

    unsigned long ulCurrentPosition=0;

    //this is where the actual searching will happen, what happens
    //here is we set the file pointer to the current position
    //is incrimented by one each pass, then we read the size of
    //the buffer into the buffer and compare it with the string
    //we're searching for, if the string is found we return the
    //position at which it is found
    while (ulCurrentPosition<ulFileSize-ulBufferSize)
    {
        //set the pointer to the current position
        fseek(pFile,ulCurrentPosition,SEEK_SET);

        //read ulBufferSize bytes from the file
        fread(lpBuffer,1,ulBufferSize,pFile);

        //if the data read matches the string we're looking for
        if (!memcmp(lpBuffer,lpszSearchString,ulBufferSize))
        {
            //free the buffer
            free(lpBuffer);

            //return the position the string was found at
            return ulCurrentPosition;
        }
        
        //incriment the current position by one
        ulCurrentPosition++;
    }

    //if we made it this far the string was not found in the file
    //so we free the buffer
    free(lpBuffer);

    //and return -1
    return -1;
} 

int main(int argc, char* argv[])
{
	FILE *in=NULL;

	unsigned long tokenno = -1,tokenyes = -1;

	int i;

	char dldino[12],dldiyes[12];

	dldino[0] = 0x4E; 
	dldino[1] = 0x4F;
	dldino[2] = 0x41;
	dldino[3] = 0x50;
	dldino[4] = 0x20;
	dldino[5] = 0x43;
	dldino[6] = 0x68;
	dldino[7] = 0x69;
	dldino[8] = 0x73;
	dldino[9] = 0x68;
	dldino[10] = 0x6D;
	dldino[11] = 0x00;

	dldiyes[0] = 0xED;
	dldiyes[1] = 0xA5;
	dldiyes[2] = 0x8D;
	dldiyes[3] = 0xBF;
	dldiyes[4] = 0x20;
	dldiyes[5] = 0x43;
	dldiyes[6] = 0x68;
	dldiyes[7] = 0x69;
	dldiyes[8] = 0x73;
	dldiyes[9] = 0x68;
	dldiyes[10] = 0x6D;
	dldiyes[11] = 0x00;

	print_header();

	if(!parse_command(argc,argv)) { print_usage(); return -1; }
	
  	in = fopen(argv[1], "r+b");
	if(!in) {
		fprintf(stderr, "ERROR: Failed to open input file: %s\n", argv[1]);
        return 1;
	  }

	tokenno = FileSearch(in, dldiyes);

	if (tokenno == -1)
		tokenyes = FileSearch(in, dldino);

	if (tokenno != -1)
	{
		fprintf(stdout,"Disabling DLDI in %s ",argv[1]);
		fseek(in,tokenno,SEEK_SET);
		for (i = 0; i < 4; i++)
		{
		fputc(dldino[i], in);
		fprintf(stdout,".");
		}
		fprintf(stdout,"done.\n");
	}
	else
	if (tokenyes != -1)
	{
		fprintf(stdout,"Enabling DLDI in %s ",argv[1]);
		fseek(in,tokenyes,SEEK_SET);
		for (i = 0; i < 4; i++)
		{
		fputc(dldiyes[i], in);
		fprintf(stdout,".");
		}
		fprintf(stdout,"done.\n");

	}
	else
		fprintf(stderr, "ERROR: You shouldn't see this. :) \n");

	fflush(in);
	fclose(in);
	return 0;
}

