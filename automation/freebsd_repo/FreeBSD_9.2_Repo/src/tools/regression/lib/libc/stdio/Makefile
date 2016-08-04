# $FreeBSD: releng/9.2/tools/regression/lib/libc/stdio/Makefile 252343 2013-06-28 16:07:20Z jhb $

TESTS=	test-fmemopen test-getdelim test-open_memstream test-open_wmemstream \
	test-perror test-print-positional test-printbasic test-printfloat \
	test-scanfloat 
CFLAGS+= -lm

.PHONY: tests
tests: ${TESTS}
	for p in ${TESTS}; do ${.OBJDIR}/$$p; done

.PHONY: clean
clean:
	-rm -f ${TESTS}
