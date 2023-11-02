#!/bin/bash

#
# debugging purpose, should be turned OFF for main production
#
#export LD_DEBUG=files

# Added upon suggestion by Adrian and Latchezar, should help when we do data processing while data deletion is ongoing
export XRD_STREAMTIMEOUT=60
export ALIEN_JDL_LPMRUNNUMBER=537901
export ALIEN_JDL_LPMINTERACTIONTYPE=pp
export ALIEN_JDL_LPMPRODUCTIONTAG=LHC23zc
export ALIEN_JDL_LPMPASSNAME=apass1_relval_itstpcmap_1
export ALIEN_JDL_LPMANCHORYEAR=2023
export IGNORE_EXISTING_SHMFILES=1

[[ -f dpl-workflow.sh ]] && chmod +x dpl-workflow.sh

if [ ! -z "$JALIEN_TOKEN_CERT" -a ! -f "$JALIEN_TOKEN_CERT" ]; then
    echo "$JALIEN_TOKEN_CERT" > tokencertJOB.pem 
    export JALIEN_TOKEN_CERT=tokencertJOB.pem 

    echo "$JALIEN_TOKEN_KEY" > tokenkeyJOB.pem 
    export JALIEN_TOKEN_KEY=tokenkeyJOB.pem
fi

echo "*************** Printing env ****************"
set;
echo "*************** Done env ****************"

# unset O2DPG_ROOT in case you find the tgz, so that it can be set again later
if [ -f "o2dpg.tgz" ]; then
    export O2DPG_ROOT=
fi

### check environment

if [ "$O2DPG_ROOT" = "" ]; then

    if [ -f "o2dpg.tgz" ]; then

	echo "Using O2DPG from tarball"
	tar zxvf o2dpg.tgz
	export O2DPG_ROOT=${PWD}/O2DPG
	
    else
	
	echo "*! ERROR: O2DPG_ROOT is not set!"
	echo "ERROR: O2DPG_ROOT is not set!" > validation_error.message
	exit
	
    fi
fi

DPGRECO=$O2DPG_ROOT/DATA/production/configurations/asyncReco/async_pass.sh

if [[ -f async_pass.sh ]]; then
    chmod +x async_pass.sh
    DPGRECO=./async_pass.sh
fi

echo "Calling '$DPGRECO $*'"
$DPGRECO $*
error=$?

if [ $error -ne 0 ]; then
    echo "*! Command '$DPGRECO $*' exited with error code $error"
    exit $error
fi

# rest of the script
rm tokenkeyJOB.pem tokencertJOB.pem &>/dev/null

exit 0
