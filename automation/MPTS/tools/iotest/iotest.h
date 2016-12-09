#ifndef _PTEST_H_
#define _PTEST_H_

#include <time.h>

#define NOTETIME(timer) 			((usetimers)? (clock_gettime(clk_id, timer)) : 0)
#define MAX_BLOCK_SIZE 			8192
#ifdef DEBUG
#define my_printf printf
#else
#define my_printf
#endif

struct stats 	{
	unsigned long long 	iocount;
	unsigned long long 	tputcount;
	unsigned long long 	tputcountrem;
	unsigned long long 	latencysecs;
	unsigned long long 	latencynsecs;
	unsigned long long 	latencysecsr;
	unsigned long long 	latencynsecsr;
	unsigned long long 	latencysecsw;
	unsigned long long 	latencynsecsw;
	unsigned long long 	maxtput;
	struct timespec 		maxlatency;
	unsigned long long 	mintput;
	struct timespec 		minlatency;
	unsigned long long 	reads;
	unsigned long long 	writes;
};

struct thread_args {
	int threadNum;
	struct stats *threadStats;
};

void DumpTimers(void);
void diff(struct timespec , struct timespec , struct timespec *);

#endif /* _PTEST_H_ */
