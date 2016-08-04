# $FreeBSD: releng/9.2/sys/modules/nfsd/Makefile 251641 2013-06-11 23:19:02Z ken $

.PATH: ${.CURDIR}/../../fs/nfsserver ${.CURDIR}/../../nfs
KMOD=	nfsd
SRCS=	vnode_if.h \
	nfs_fha.c \
	nfs_fha_new.c \
	nfs_nfsdserv.c \
	nfs_nfsdcache.c \
	nfs_nfsdkrpc.c \
	nfs_nfsdsocket.c \
	nfs_nfsdstate.c \
	nfs_nfsdsubs.c \
	nfs_nfsdport.c \
	opt_ufs.h \
	opt_nfs.h \
	opt_inet6.h \
	opt_kgssapi.h

.include <bsd.kmod.mk>
