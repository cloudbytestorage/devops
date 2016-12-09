#include <stdio.h>
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <pthread.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>
#include <dirent.h>
#include <string.h>
#include <fcntl.h>
#include "iotest.h"

int ActualWork(int threadNum, int myFd, struct stats *threadStats, char ** buf, int *bufsize);
int PrepareWork(int threadNum);
void *worker(void *arg);
void *listworker(void *arg);
void FinalResults(struct thread_args *args);
void Usage(char *argv[]);
void ParseOptions(int argc, char *argv[]);


int 		iterations = 1000;
int 		numthreads = 1;
int 		usetimers = 1;
clockid_t	clk_id = CLOCK_REALTIME;
char		*dirtoscan;
int 		listInterval = 1;
int 		lister_exit;
struct timespec 	overallTime1, overallTime2, overalldifftime;
int 		workready = 0;
pthread_mutex_t readymutex = PTHREAD_MUTEX_INITIALIZER;
int             operation = 0, operationType = 0, operationSz = 4096;
off_t		fileSz = 65536;
int 		timetorun = 0;
char 		*resultsfilename;
int		maxRandFileSz = 5 * 1024 * 1024;

void diff(struct timespec start, struct timespec end, struct timespec *temp)
{
	if ((end.tv_nsec-start.tv_nsec) < 0) {
		temp->tv_sec = end.tv_sec - start.tv_sec - 1;
		temp->tv_nsec = 1000000000 + end.tv_nsec - start.tv_nsec;
	} else {
		temp->tv_sec = end.tv_sec - start.tv_sec;
		temp->tv_nsec = end.tv_nsec - start.tv_nsec;
	}

	return;
}

int ActualWork(int threadNum, int myFd, struct stats *threadStats, char ** buf, int *bufsize)
{
	off_t offset, curOffset;
	int	optype, size, opex;
	int 	syscall_err = 0, syscall_err1, syscall_err2;
	struct  timespec time1, time2, difftime;

	/* offset */
	if (operationType == 1)	{
		offset = ((off_t)rand() % (fileSz / (off_t)(operationSz? operationSz : 4096))) * (off_t)(operationSz? operationSz : 4096);
		syscall_err = lseek(myFd, offset, SEEK_SET);
		if (syscall_err == -1)	{
			return -1;
		}
	}

	/* size */
	if (operationSz == 0)	{
		size = rand() % (((maxRandFileSz > fileSz)? fileSz : maxRandFileSz) + 1);
	}
	else	{
		size = operationSz;
	}

	/* adjust size based on offset if any */
	curOffset = lseek(myFd, 0, SEEK_CUR);
	if (curOffset == -1)	{
		syscall_err = -2;
		goto Return;
	}
	else if (curOffset == fileSz) 	{
		syscall_err = lseek(myFd, 0, SEEK_SET);
		if (syscall_err == -1) 	{
			syscall_err = -5;
			goto Return;
		}
		curOffset = 0;
	}
	if (size + curOffset > fileSz)	{
		/* size can be random, adjust size */
		if (operationSz == 0)	{
			size = fileSz - curOffset;
		}
		/* offset can be random, adjust offset */
		/* size and offset are not random, adjust offset */
		else 	{
			offset = fileSz - operationSz;
			syscall_err = lseek(myFd, offset, SEEK_SET);
			if (syscall_err == -1)	{
				syscall_err = -3;
				goto Return;
			}
		}
	}	

	/* buf allocation optimization */
	if (*bufsize < size) 	{
		if (*buf != NULL)
			free(*buf);
		*buf = malloc(size);
		*bufsize = size;
		memset(*buf, '4', *bufsize);
	}

	/* perform the operation */
	if (operation == 0)	{		
		syscall_err1 = NOTETIME(&time1);
		syscall_err = read(myFd, *buf, size);
		syscall_err2 = NOTETIME(&time2);
		threadStats->reads ++;
		opex = 1;
	} else if (operation == 100) {
		syscall_err1 = NOTETIME(&time1);
		syscall_err = write(myFd, *buf, size);
		syscall_err2 = NOTETIME(&time2);
		threadStats->writes ++;
		opex = 0;
	}
	else 	{
		optype = rand() % 100 + 1;
		if (optype <= operation) 	{
			syscall_err1 = NOTETIME(&time1);
			syscall_err = write(myFd, *buf, size);
			syscall_err2 = NOTETIME(&time2);
			threadStats->writes ++;
			opex = 0;
		}
		else 	{
			syscall_err1 = NOTETIME(&time1);
			syscall_err = read(myFd, *buf, size);
			syscall_err2 = NOTETIME(&time2);
			threadStats->reads ++;
			opex = 1;
		}
	}

	/* process the errors */
	if (syscall_err != size)
		syscall_err = -4;
	else
		syscall_err = 0;
	if (syscall_err1 || syscall_err2) 	{
		syscall_err = -5;
		goto Return;
	}

	/* update stats */
	threadStats->iocount ++;
	threadStats->tputcount += size / 1024;
	threadStats->tputcountrem += size % 1024;
	threadStats->tputcount += threadStats->tputcountrem / 1024;
	threadStats->tputcountrem %= 1024;
	diff(time1, time2, &difftime);
	threadStats->latencynsecs += difftime.tv_nsec;
	threadStats->latencysecs += difftime.tv_sec;
	threadStats->latencysecs += threadStats->latencynsecs /1000000000;
	threadStats->latencynsecs %= 1000000000;
	/* update read/write time */
	if (opex == 1)	{
		threadStats->latencynsecsr += difftime.tv_nsec;
		threadStats->latencysecsr += difftime.tv_sec;
		threadStats->latencysecsr += threadStats->latencynsecsr /1000000000;
		threadStats->latencynsecsr %= 1000000000;
	}
	else	{
		threadStats->latencynsecsw += difftime.tv_nsec;
		threadStats->latencysecsw += difftime.tv_sec;
		threadStats->latencysecsw += threadStats->latencynsecsw /1000000000;
		threadStats->latencynsecsw %= 1000000000;
	}
	if (threadStats->maxlatency.tv_sec < difftime.tv_sec) 	{
		threadStats->maxlatency.tv_sec = difftime.tv_sec;
		threadStats->maxlatency.tv_nsec = difftime.tv_nsec;
	}
	else if (threadStats->maxlatency.tv_sec == difftime.tv_sec) 	{
		if (threadStats->maxlatency.tv_nsec < difftime.tv_nsec) 	{
			threadStats->maxlatency.tv_sec = difftime.tv_sec;
			threadStats->maxlatency.tv_nsec = difftime.tv_nsec;
		}
	}
	if (threadStats->minlatency.tv_sec > difftime.tv_sec) 	{
		threadStats->minlatency.tv_sec = difftime.tv_sec;
		threadStats->minlatency.tv_nsec = difftime.tv_nsec;
	}
	else if (threadStats->minlatency.tv_sec == difftime.tv_sec) 	{
		if (threadStats->minlatency.tv_nsec < difftime.tv_nsec) 	{
			threadStats->minlatency.tv_sec = difftime.tv_sec;
			threadStats->minlatency.tv_nsec = difftime.tv_nsec;
		}
	}
	if (threadStats->maxtput < (unsigned int)size) 	{
		threadStats->maxtput = size;
	}	
	if (threadStats->mintput > (unsigned int)size) 	{
		threadStats->mintput = size;
	}

Return:	
	return syscall_err;
}

int PrepareWork(int threadNum)
{
	char my_path[1024];
	struct stat buf;
	int fd, syscall_err;
	int i, blkSz = MAX_BLOCK_SIZE;
	char *block = NULL;

	sprintf(my_path, "%s/testfile%d", dirtoscan, threadNum);
	fd = open(my_path, O_RDWR | O_CREAT, 00777);
	if (fd < 0)	{
		return -1;
	}

	syscall_err = fstat(fd, &buf);
	if (syscall_err)	{
		return -2;
	}

	if (buf.st_size < fileSz)	{
		syscall_err = lseek(fd, buf.st_size, SEEK_SET);
		if (syscall_err == -1)	{
			return -4;
		}
		assert(block = malloc(blkSz));
		memset(block, '3', blkSz); 
		for (i = 0;i < fileSz; i += blkSz)	{
			syscall_err = write(fd, block, blkSz);
			if (syscall_err < blkSz)	{
				return -3;
			}
		}
	}

	if (block)
		free(block);

	return fd;
}

void *worker(void *arg)
{
	struct thread_args locarg = *((struct thread_args *)arg);
	struct timespec time1, time2, difft;
	int syscall_err, fn_err, i;
	int myFd;
	int bufsize = 0;
	char *buf = NULL;

	fn_err = PrepareWork(locarg.threadNum);
	if (fn_err < 0)	{
		printf("Worker#%d errored out, Unable to prepare work (err - %d, file size - %ld)\n", locarg.threadNum, fn_err, fileSz);
		return NULL;
	}
	myFd = fn_err;

	/* wait for all workers to complete */
	pthread_mutex_lock(&readymutex);
	workready ++;
	pthread_mutex_unlock(&readymutex);
	while (workready != numthreads) 	{
		sleep(1);
	}

	NOTETIME(&overallTime1);

	if (timetorun != 0) 	{
		syscall_err = NOTETIME(&time1);
		if (syscall_err) 	{
			printf("Worker#%d error in syscall clock_gettime: %d %d\n", locarg.threadNum, syscall_err, errno);
			goto Return;
		}
	}

	i = 0;
	while (1)	{
		fn_err = ActualWork(locarg.threadNum, myFd, locarg.threadStats, &buf, &bufsize);
		if (fn_err)	{
			printf("Worker#%d errored out, no more loops (err - %d, loop - %d))\n", locarg.threadNum, fn_err, i);
			break;
		}
		i ++;
		if (timetorun != 0) 	{
			syscall_err = NOTETIME(&time2);
			if (syscall_err) 	{
				printf("Worker#%d error in syscall clock_gettime: %d %d\n", locarg.threadNum, syscall_err, errno);
				goto Return;
			}

			diff(time1, time2, &difft);
			if (difft.tv_sec >= timetorun) 	{
				break;
			}
		}
		else if (i >= iterations) 	{
			break;
		}
	}
	
	syscall_err = NOTETIME(&time2);
	if (syscall_err) 	{
		printf("Worker#%d error in syscall clock_gettime: %d %d\n", locarg.threadNum, syscall_err, errno);
		goto Return;
	}
	
Return:
	if (buf)
		free(buf);
	close(myFd);

	return NULL;
}

void *listworker(void *arg)
{
	struct thread_args *locarg = arg;
	int i;
	unsigned long long previocount = 0;
	unsigned long long prevtputcount = 0;
	unsigned long long prevlatencysecs = 0;
	unsigned long long prevlatencynsecs = 0;
	unsigned long long prevlatencysecsr = 0;
	unsigned long long prevlatencynsecsr = 0;
	unsigned long long prevlatencysecsw = 0;
	unsigned long long prevlatencynsecsw = 0;
	unsigned long long prevreads = 0;
	unsigned long long prevwrites = 0;
	long long iocount = 0;
	long long tputcount = 0;
	long long latencysecs = 0;
	long long latencynsecs = 0;
	unsigned long long latencyusecs = 0;
	long long latencysecsr = 0;
	long long latencynsecsr = 0;
	unsigned long long latencyusecsr = 0;
	long long latencysecsw = 0;
	long long latencynsecsw = 0;
	unsigned long long latencyusecsw = 0;
	long long reads = 0;
	long long writes = 0;
	int printHeader = 20;
	
	while (lister_exit == 0) 	{
		sleep(listInterval);
		iocount = 0; iocount -= previocount;
		tputcount = 0; tputcount -= prevtputcount;
		latencynsecs = 0; latencynsecs -= prevlatencynsecs;
		latencysecs = 0; latencysecs -= prevlatencysecs;
		latencynsecsr = 0; latencynsecsr -= prevlatencynsecsr;
		latencysecsr = 0; latencysecsr -= prevlatencysecsr;
		latencynsecsw = 0; latencynsecsw -= prevlatencynsecsw;
		latencysecsw = 0; latencysecsw -= prevlatencysecsw;
		reads = 0; reads -= prevreads;
		writes = 0; writes -= prevwrites;
		for (i = 0; i < numthreads; i++) 	{
			iocount += locarg[i].threadStats->iocount;
			tputcount += locarg[i].threadStats->tputcount;
			latencysecs += locarg[i].threadStats->latencysecs;
			latencynsecs += locarg[i].threadStats->latencynsecs;
			latencysecsr += locarg[i].threadStats->latencysecsr;
			latencynsecsr += locarg[i].threadStats->latencynsecsr;
			latencysecsw += locarg[i].threadStats->latencysecsw;
			latencynsecsw += locarg[i].threadStats->latencynsecsw;
			reads += locarg[i].threadStats->reads;
			writes += locarg[i].threadStats->writes;
		}
		latencyusecs = latencynsecs / 1000;
		latencyusecs += latencysecs * 1000000;
		latencyusecsr = latencynsecsr / 1000;
		latencyusecsr += latencysecsr * 1000000;
		latencyusecsw = latencynsecsw / 1000;
		latencyusecsw += latencysecsw * 1000000;
		if (iocount != 0) 	{
			latencyusecs /= iocount;
		}
		if (reads != 0) 	{
			latencyusecsr /= reads;
		}
		if (writes != 0) 	{
			latencyusecsw /= writes;
		}
		if (printHeader == 20) 	{
			printf("\tInterval\tIOs\tThroughput(KB/sec)\tAvg. Latency\t\tReadLat.\t\tWriteLat.\t\tReads\t\tWrites\n");
			printHeader = 0;
		}
		else 
			printHeader ++;
		printf("\t%d\t\t%lld\t%lld\t\t\t%lld\t\t\t%lld\t\t\t%lld\t\t\t%lld\t\t%lld\n", listInterval, iocount, (tputcount/listInterval),
			       	latencyusecs, latencyusecsr, latencyusecsw, reads, writes);
		previocount += iocount;
		prevtputcount += tputcount;
		prevlatencynsecs += latencynsecs;
		prevlatencysecs += latencysecs;
		prevlatencynsecsr += latencynsecsr;
		prevlatencysecsr += latencysecsr;
		prevlatencynsecsw += latencynsecsw;
		prevlatencysecsw += latencysecsw;
		prevreads += reads;
		prevwrites += writes;
	}

	return NULL;
}

void FinalResults(struct thread_args *args)
{
	int fd = 0, i;
	char writeBuf[2048];

	/* open sesame */
	fd = open(resultsfilename, O_CREAT | O_TRUNC | O_RDWR, 00777);
	if (fd < 0) 	{
		printf("Error opening results file mentioned : (err - %d, file - %s)\n", errno, resultsfilename);
		return;
	}

	/*print job data */
	sprintf(writeBuf, "%s,%d\n%s,%d\n%s,%d\n%s,%s\n%s,%d\n%s,%ld\n%s,%d\n%s,%d\n%s,%d\n%s,%d\n%s,%s\n", "Iterations", iterations, "#Threads", numthreads, "Timer", usetimers, "Path", dirtoscan, "Listing Interval", listInterval, "File Size", fileSz, "Operation", operation, "Operation Type", operationType, "Operation Size", operationSz, "Time to run", timetorun, "Results @", resultsfilename);
	write(fd, writeBuf, strlen(writeBuf));
	sprintf(writeBuf, "%s,%ld,%ld\n", "Total Time (sec/nsec)", overalldifftime.tv_sec, overalldifftime.tv_nsec);
	write(fd, writeBuf, strlen(writeBuf));
	
	/* print header */
	sprintf(writeBuf, "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n", "IO Count", "Throughput (KB)", "Throughput Bytes) remainder", "Latency Secs", "Latency nSecs", "Max Throughput", "Min Throughput", "Max Latency (secs)", "Max Latency (nsecs)", "Min Latency (secs)", "Min Latency (nsecs)", "Reads", "Writes");
	write(fd, writeBuf, strlen(writeBuf));
	
	/* print per thread stats */
	for (i = 0; i < numthreads; i++) 	{
		sprintf(writeBuf, "%lld,%lld,%lld,%lld,%lld,%lld,%lld,%ld,%ld,%ld,%ld,%lld,%llu\n", args[i].threadStats->iocount, args[i].threadStats->tputcount, args[i].threadStats->tputcountrem, args[i].threadStats->latencysecs, args[i].threadStats->latencynsecs, args[i].threadStats->maxtput, args[i].threadStats->mintput, args[i].threadStats->maxlatency.tv_sec, args[i].threadStats->maxlatency.tv_nsec, args[i].threadStats->minlatency.tv_sec, args[i].threadStats->minlatency.tv_nsec, args[i].threadStats->reads, args[i].threadStats->writes);
		write(fd, writeBuf, strlen(writeBuf));
	}

	close(fd);

}

void Usage(char *argv[])
{
	printf("Command: %s\n", argv[0]);
	printf("Usage: %s [Options] <path>\n", argv[0]);
	printf("Options and defaults:\n");
	printf("\tt - Thread count (default: 1)\n");
	printf("\ti - Iterations per thread (defualt: 1000)\n");
	printf("\tT - Seconds to execute (mutually exclusive from -i option only one should be specified. Default is the -i option with 1000 iterations.\n");
	printf("\ts - File size in bytes, each thread will create and operate on a file as big as this size (default: 65536 bytes)\n");
	printf("\tW - Write %%age,%%age of write operation to perform. Set to 100 only writes are done, set to any other number, then proportinal writes are done, set to 0 only reads are done (default: 0 (all reads))\n");
	printf("\tr - Sets random read/write behaviour, (default: off (sequential))\n");
	printf("\tb - Sets per operation read/write size. Set to 0, does random sized reads/writes each IO, set to a number, does as many bytes read/write (default: 4096 bytes)\n");
	printf("\tl - Listing interval, lists statistics every n seconds as specified. Set to 0 to not list while running (default: 1)\n");
	printf("\to - Output file name to store results at end of run (default: Not stored)\n");
	printf("\t<path> - Path in the filesystem of choice to test, where files will be generated and IO will be tested (default: NONE, REQUIRED paramater)\n");
}

void ParseOptions(int argc, char *argv[])
{
	int c, errflg = 0;
	int iterSpecified = 0, timeSpecified = 0, printUsage = 0;
	extern char *optarg;
	extern int optind, optopt;
	
	while ((c = getopt(argc, argv, "ht:i:T:s:W:rb:l:o:")) != -1) {
		switch(c) {
			case 'h':
				printUsage = 1;
			break;
			case 't':
				numthreads = atoi(optarg);
				if (numthreads <= 0) 	{
					errflg ++;
					printf("Option \'-t\' requires positive number of threads, passed in option is either less than 0, or incorrect (value: %s)\n", optarg);
				}
			break;
			case 'i':
				iterSpecified = 1;
				iterations = atoi(optarg);
				if (iterations <= 0) 	{
					errflg ++;
					printf("Option \'-i\' requires positive number of iterations, passed in option is either less than 0, or incorrect (value: %s)\n", optarg);
				}				
				if (timeSpecified) 	{
					errflg ++;
					printf("Option \'-T\' and \'-i\' cannot be specified togeather, only one of the options should be used\n");
				}
			break;
			case 'T':
				timeSpecified = 1;
				timetorun = atoi(optarg);
				if (timetorun <= 0) 	{
					errflg ++;
					printf("Option \'-T\' requires positive number of seconds, passed in option is either less than 0, or incorrect (value: %s)\n", optarg);
				}
				if (iterSpecified) 	{
					errflg ++;
					printf("Option \'-T\' and \'-i\' cannot be specified togeather, only one of the options should be used\n");
				}
			break;
			case 's':
				fileSz = atol(optarg);
				if (fileSz <= 0) 	{
					errflg ++;
					printf("Option \'-s\' requires positive file size, passed in option is either less than 0, or incorrect (value: %s)\n", optarg);
				}
			break;
			case 'W':
				operation = atoi(optarg);
				if (operation < 0 || operation > 100) 	{
					errflg ++;
					printf("Option \'-R\' requires positive number between 0 - 100 (as it is used as a percentage), passed in option is incorrect (value: %s)\n", optarg);
				}
			break;
			case 'r':
				operationType = 1;
			break;
			case 'b':
				operationSz = atoi(optarg);
				if (operationSz < 0) 	{
					errflg ++;
					printf("Option \'-b\' requires 0 or a positive number to perform random sized or fixed size IO, passed in option is incorrect (value: %s)\n", optarg);
				}
			break;
			case 'l':
				listInterval = atoi(optarg);
				if (listInterval < 0) 	{
					errflg ++;
					printf("Option \'-l\' requires 0 or a positive number to perform interval based output of statistics, passed in option is incorrect (value: %s)\n", optarg);
				}
			break;
			case 'o':
				resultsfilename = malloc(strlen(optarg + 1));
				if (resultsfilename == NULL)	{
					printf("Error aloating memory for results file path\n");
					errflg ++;
					break;
				}
				strcpy(resultsfilename, optarg);
			break;
			case ':':
				printf("Option -%c requires an operand\n", optopt);
				errflg++;
			break;
			case '?':
				printf("Unrecognized option: -%c\n", optopt);
				errflg++;	
		}
	}
	
	if (optind >= argc) 	{
		errflg ++;
		printf("Option <path> not specified, this details which path to execute IO on\n");
	}
	else  if ((optind + 1) != argc){		
		errflg ++;
		printf("Extra options specified in command line, remove trailing options or characters\n");
	}
	else 	{
		dirtoscan = malloc(strlen(argv[optind] + 1));
		if (dirtoscan == NULL)	{
			errflg ++;
			printf("Error aloating memory for path to perform IO operations on\n");
		} else 	{
			strcpy(dirtoscan, argv[optind]);
			if(access(dirtoscan, F_OK | W_OK)) 	{
				errflg ++;
				printf("User/Program does not have write access to path, or path does not exist where IO operations need to be performed, path: %s\n", dirtoscan);
			}
		}
	}
	
	if (errflg) {
		printf("\nErrors enountered in parsing command line, try \'%s -h\' for more details and help on usage\n\n", argv[0]);
		if (printUsage) 
			Usage(argv);
		exit(1);
	}

	if (printUsage) 	{
		Usage(argv);
		exit(0);
	}

	return;
}

int main(int argc, char **argv)
{
	int i;
	pthread_t *t;
	struct thread_args *args;
	pthread_t lister;

	/* Get the options passed or run with defaults */
	ParseOptions(argc, argv);
	
	/* create # bucket for threads */
	t = (pthread_t *)calloc(numthreads, sizeof(pthread_t));
	args = (struct thread_args *)calloc(numthreads, sizeof(struct thread_args));
	if (!t || !args) {
		fprintf(stderr, "Unable to allocate memory, bye!!!\n");
		return -1;
	}

	/* Parse thread types and fill arguments for each thread */
	for (i = 0; i < numthreads; i++)	{
		args[i].threadNum = i;
		assert(args[i].threadStats = calloc(1, sizeof(struct stats)));
		args[i].threadStats->mintput = fileSz;
		args[i].threadStats->minlatency.tv_sec = 100000;
		args[i].threadStats->minlatency.tv_nsec = 1000000000;
	}

	/* Job start */
	printf("JOB: #threads %d : #iterations %d : #file size %ld\n", numthreads, iterations, fileSz);
	printf("PATH: %s\n", dirtoscan);
	printf("******** \tStarted \t\t********\n");

	/* create the listing thread */
	if (listInterval != 0)
	{
		lister_exit = 0;
		assert(!pthread_create(&(lister), NULL, listworker, (void *)args));
	}
	
	/* Create the threads */
	for (i = 0; i < numthreads; i++) 
		assert(!pthread_create(&(t[i]), NULL, worker, (void *)&(args[i])));

	/* wait for the completion of all the threads */
	for (i = 0; i < numthreads; ++i)
		assert(!pthread_join(t[i], NULL));

	NOTETIME(&overallTime2);
	diff(overallTime1, overallTime2, &overalldifftime);

	if (listInterval != 0)
	{
		lister_exit = 1;
		pthread_join(lister, NULL);
	}

	printf("******** \tCompleted \t\t********\n");

	/* Final results time */
	if (resultsfilename != NULL)
		FinalResults(args);

	/* cleanup */
	free(t);
	for (i = 0; i < numthreads; i++) 	{
		free(args[i].threadStats);
	}

	free(args);
	free(dirtoscan);
	free(resultsfilename);

	return 0;
}
