#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int rgbv[]={93, 43, 208, 158, 255, 230};

int main()
{
    char byte[32];

    int fd = open("/dev/ttyUSB0", O_RDWR);
    write(fd, "RS \r", 4);
		usleep(500e3);
    read(fd, &byte[0], 32);
    printf("R => %s\n", byte);

		sprintf(byte, "TC %d %d %d %d %d %d \r",255-rgbv[0],255-rgbv[1],255-rgbv[2],255-rgbv[3],255-rgbv[4],255-rgbv[5]);
		printf("%s\n",byte );
		write(fd, byte, 23);

		while(1)
		{
			char end=0;
			int i=0;
			while(end!='\r')
			{
				read(fd, &end, 1);
				byte[i++]=end;
			}
			byte[i]='\0';
	    printf("R => %s\n", byte);
		}


    return 0;
}
