# $FreeBSD: releng/9.2/secure/libexec/ssh-keysign/Makefile 251134 2013-05-30 12:25:37Z des $

PROG=	ssh-keysign
SRCS=	ssh-keysign.c readconf.c roaming_dummy.c
MAN=	ssh-keysign.8
CFLAGS+=-I${SSHDIR} -include ssh_namespace.h
BINMODE=4555

DPADD=	${LIBSSH} ${LIBCRYPT} ${LIBCRYPTO} ${LIBZ}
LDADD=	-lssh -lcrypt -lcrypto -lz

.include <bsd.prog.mk>

.PATH:	${SSHDIR}

${OBJS} ${POBJS} ${SOBJS}: ssh_namespace.h
