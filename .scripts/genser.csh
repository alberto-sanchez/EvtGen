# POSIX shell settings for GENSER integrators
#

setenv CVSROOT :kserver:simu.cvs.cern.ch:/cvs/simu

echo ""
echo "CVSROOT is set to $CVSROOT"

echo ""
echo "Path to GENSER web pages:"

echo ""
echo "Path to GENSER3 build area:"

setenv GBUILD $MCGREPLICA/.work/GENSER-BUILD/build

echo "GBUILD=${GBUILD}"
echo ""
echo "Build directory for a generator is then"
echo "\${GBUILD}/pkgsrc/MCGenerators/generator_name"
echo

# Paths to bmake and other pkgsrc routines:
#
setenv PATH ${GBUILD}/bin:${GBUILD}/sbin:${PATH}

# SLC5 has g77 installed so we must forcibly
# set gfortran as a default fortran compiler
# to get slc5_<arch>_gcc41 platform:
#
if test -s /etc/redhat-release ; then
	echo ""
	echo "Good news: you're running RedHat derived OS"
	if test "x`grep 'CERN SLC release 5' < /etc/redhat-release`" != "x"  ; then
		echo "BAD news: the OS is SLC5"
		export FC=gfortran
		export F77=${FC}
		export CC=gcc
		export CXX=g++
	fi
fi

_info_str=""

if test "x${FC}" != "x" ; then
	_info_str="$_info_str FC=${FC}"
fi
if test "x${F77}" != "x" ; then
	_info_str="$_info_str F77=${F77}"
fi
if test "x${CC}" != "x" ; then
	_info_str="$_info_str CC=${CC}"
fi
if test "x${CXX}" != "x" ; then
	_info_str="$_info_str CXX=${CXX}"
fi

if test "x$_info_str" != "x" ; then
	echo ""
	echo "ATTENTION: the following variables are forcibly exported:" 
	echo ""
	echo "$_info_str"
	echo ""
fi
