#include <sys/param.h>
#include <sys/module.h>
#include <sys/kernel.h>
#include <sys/systm.h>
#include <sys/malloc.h>

/* sys/something/foo_main.c */
MALLOC_DECLARE(M_FOOBUF);
MALLOC_DEFINE(M_FOOBUF, "foobuffers", "Buffers to foo data into the ether");

void fn1(void);
int *a[100000];
int n = 50 * 1024;
void fn1(void)
{
	int i;
	int size = 1024*1024;
	if(n > 90000) n = 90000;
	for(i = 0; i < n; i++)
		a[i] = (int *)malloc(size, M_FOOBUF, M_NOWAIT);
}

void fn2(void);
void fn2(void)
{
	int i;
	for(i = 0; i< n; i++)
		free(a[i], M_FOOBUF);
}

/* The function called at load/unload. */
static int event_handler(struct module *module, int event, void *arg) {
        int e = 0; /* Error, 0 for normal return status */
        switch (event) {
        case MOD_LOAD:
               // uprintf("Hello Free Software Magazine Readers! \n");
                uprintf("Allocating Memory -- %dMB \n", n);
		fn1();
                break;
        case MOD_UNLOAD:
		fn2();
                //uprintf("Bye Bye FSM reader, be sure to check http://freesoftwaremagazine.com !\n");
                uprintf("Freeing Memory -- %dMB \n", n);
                break;
        default:
                e = EOPNOTSUPP; /* Error, Operation Not Supported */
                break;
        }
       
        return(e);
}

/* The second argument of DECLARE_MODULE. */
static moduledata_t hello_conf = {
    "hello_fsm",    /* module name */
     event_handler,  /* event handler */
     NULL            /* extra data */
};


DECLARE_MODULE(hello_fsm, hello_conf, SI_SUB_DRIVERS, SI_ORDER_MIDDLE);

