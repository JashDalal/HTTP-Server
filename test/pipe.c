#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <errno.h>
int main(int argc, char *argv[]) {
	int fd, n, i;
	char buf[128];
	int pfd[2];
	
	pipe(pfd);
	// pfd[0] is read end, pfd[1] is write endA
	write(pfd[1], "hello", 5);
	read(pfd[0], buf, 5);
	
}
