/*-
 * Copyright (c) 2008 David Schultz <das@FreeBSD.ORG>
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

#include <sys/cdefs.h>
__FBSDID("$FreeBSD: releng/9.2/lib/msun/ld80/invtrig.c 181074 2008-07-31 22:41:26Z das $");

#include "invtrig.h"

/*
 * asinl() and acosl()
 */
const long double
pS0 =  1.66666666666666666631e-01L,
pS1 = -4.16313987993683104320e-01L,
pS2 =  3.69068046323246813704e-01L,
pS3 = -1.36213932016738603108e-01L,
pS4 =  1.78324189708471965733e-02L,
pS5 = -2.19216428382605211588e-04L,
pS6 = -7.10526623669075243183e-06L,
qS1 = -2.94788392796209867269e+00L,
qS2 =  3.27309890266528636716e+00L,
qS3 = -1.68285799854822427013e+00L,
qS4 =  3.90699412641738801874e-01L,
qS5 = -3.14365703596053263322e-02L;

/*
 * atanl()
 */
const long double atanhi[] = {
	 4.63647609000806116202e-01L,
	 7.85398163397448309628e-01L,
	 9.82793723247329067960e-01L,
	 1.57079632679489661926e+00L,
};

const long double atanlo[] = {
	 1.18469937025062860669e-20L,
	-1.25413940316708300586e-20L,
	 2.55232234165405176172e-20L,
	-2.50827880633416601173e-20L,
};

const long double aT[] = {
	 3.33333333333333333017e-01L,
	-1.99999999999999632011e-01L,
	 1.42857142857046531280e-01L,
	-1.11111111100562372733e-01L,
	 9.09090902935647302252e-02L,
	-7.69230552476207730353e-02L,
	 6.66661718042406260546e-02L,
	-5.88158892835030888692e-02L,
	 5.25499891539726639379e-02L,
	-4.70119845393155721494e-02L,
	 4.03539201366454414072e-02L,
	-2.91303858419364158725e-02L,
	 1.24822046299269234080e-02L,
};

const long double pi_lo = -5.01655761266833202345e-20L;