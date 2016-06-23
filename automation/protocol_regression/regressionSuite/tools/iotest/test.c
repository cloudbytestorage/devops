
#include <stdlib.h>
#include <stdio.h>

off_t fileSz = 107374313472;
int operationSz = 8192;
off_t offset,rnd,sectors;
int myrnd = 0;

main()
{
	sectors = fileSz / (off_t)(operationSz? operationSz : 4096);
	while (1) {
		myrnd = rand();
		rnd = (off_t)(myrnd) % (fileSz / (off_t)(operationSz? operationSz : 4096));
		offset = (rnd) * (off_t)(operationSz? operationSz : 4096);
		printf("Offset: %jd : %jd : %jd : %d\n", offset, rnd, sectors, myrnd);
	}
}
