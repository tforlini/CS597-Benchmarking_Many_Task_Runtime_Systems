#include "main.decl.h"

#include "main.h"
#include "hello.decl.h"


/* readonly */ CProxy_Main mainProxy;
/* readonly */ int nSleep;


Main::Main(CkArgMsg* msg) {

  
  doneCount = 0;    
  numElements = 5;  
  
  if (msg->argc > 1)
    numElements = atoi(msg->argv[1]);
  if (msg->argc > 2)
    nSleep = atoi(msg->argv[2]);
  delete msg;

  CkPrintf("Running Sleep(%d) with %d elements using %d processors.\n",nSleep,numElements, CkNumPes());

  mainProxy = thisProxy;
  CProxy_Hello helloArray = CProxy_Hello::ckNew(numElements);
  helloArray.sleep(nSleep);

}

Main::Main(CkMigrateMessage* msg) { }

void Main::done() {

  doneCount++;
  if (doneCount >= numElements){
   double time2 = CkWallTimer();
    CkPrintf("Total Time: %f\n",time2);
    CkExit();

}
}


#include "main.def.h"

