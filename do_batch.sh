#!/bin/sh

DEBUG=$1

# 4, 6, 500, do.fr

BATCH=0
MAX_BATCHES=1

BATCH_SIZE=1

BATCH_FILE=do.test

do_massage() {
    sed -n "${1},${2}p" $3 | sed -e 's?^?    http://sure.grafware.com?' -e 's/%/%%/g' > do_all.urls
}

do_batch() {
    set -x
    START=`expr $1 \* $BATCH_SIZE + 1`
    END=`expr $START + $BATCH_SIZE - 1`
    do_massage $START $END $BATCH_FILE > do_all.urls
    MAX=`cat do_all.urls | wc -l`
    if [ $MAX -gt 0 ]; then
        cat remote.cfg.in do_all.urls settings.cfg > remote.cfg
        bin/funnelweb --pipeline=remote.cfg --crawler:max=$MAX --crawler:debug
    fi
    if [ $MAX -eq $BATCH_SIZE ]; then
        return 0
    else
        return 1
    fi
}

do_loop() {
    while :
    do
        echo '+++++++ START', $BATCH `date`
        do_batch $BATCH
        if [ $? -ne 0 ]; then
            return
        fi
        BATCH=`expr $BATCH + 1`
        if [ $BATCH -ge $MAX_BATCHES ]; then
            echo "MAX_BATCHES DONE $BATCH " `date`
            return
        fi
    done 
    echo '--------- DONE', `date`
}

SUFFIX=`echo $BATCH_FILE | sed -e 's:/:_:g'`
OUT=out.$SUFFIX.$BATCH_SIZE.$BATCH
if [ -z "$DEBUG" ]; then
    do_loop >> $OUT 2>&1 &
    sleep 5
    tail -f $OUT
else
    do_loop 
fi
