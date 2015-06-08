#include "hello.decl.h"

#include "hello.h"
#include "main.decl.h"
#include "main.h"
#include <ctime>
#include <cstdio>


extern /* readonly */ CProxy_Main mainProxy;


Hello::Hello() {

}

Hello::Hello(CkMigrateMessage *msg) { }


void Hello ::sayHi(int from) {

  CkPrintf("\"Hello\" from Hello chare # %d on processor %d (told by %d).\n",thisIndex, CkMyPe(), from);
  mainProxy.done();
}

void Hello ::sleep(int nSleep) {

    double time1 = CkWallTimer();
    usleep(nSleep*1000);
    double time2 = CkWallTimer();
    CkPrintf("%f\n",(time2-time1));
    mainProxy.done();
}

#include "hello.def.h"

