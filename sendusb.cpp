#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string>
#include <iostream>

int rgbv[]={93, 43, 208, 158, 255, 230};
char  temp;
int  i=0;
char byte[64];
char msg[9];
char *pch;

int main()
{

    int fd = open("/dev/ttyUSB0", O_RDWR);

		// restart camera
    write(fd, "RS \r", 4);
		usleep(500e3);
    read(fd, &byte[0], 32);
    printf("R => %s\n", byte);
		// ask camera to track
		sprintf(byte, "TC %d %d %d %d %d %d \r",255-rgbv[0],255-rgbv[1],255-rgbv[2],255-rgbv[3],255-rgbv[4],255-rgbv[5]);

		i=0;
		temp=0;
		while(temp!='\r')
			temp=byte[i++];
		write(fd, byte, i);

		// proccess data
		while(1)
		{
			i=0;
			temp=0;
			while(temp!='\r')
			{
				read(fd, &temp, 1);
				byte[i++]=temp;
			}
			byte[i]='\0';

			pch = strtok(byte," ");
			i=0;
			while(pch != NULL)
		  {
				msg[i++]=atoi(pch);
		    //printf ("%d -> %d\n",i++,msg[i]);
		    pch = strtok(NULL, " ");
		  }
			// Default Type T packet
			// T mx my x1 y1 x2 y2 pixels confidence
			printf("coord (%d\t%d)\n",msg[1],msg[2] );
		}

    return 0;
}
