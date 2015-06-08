#include <cstdio>
#include <cassert>
#include <cstdlib>
#include <ctime>
#include <unistd.h>
#include "legion.h"
using namespace LegionRuntime::HighLevel;


enum TaskIDs {
  TOP_LEVEL_TASK_ID,
  HELLO_WORLD_INDEX_ID,
};

void top_level_task(const Task *task,
		    const std::vector<PhysicalRegion> &regions,
		    Context ctx, HighLevelRuntime *runtime)
{
  clock_t startTime = clock();

  int num_points = 4;
  int nSleep = 0;
  const InputArgs &command_args = HighLevelRuntime::get_input_args();
  if (command_args.argc > 1)
  {
    num_points = atoi(command_args.argv[1]);
    assert(num_points > 0);
  }

  if (command_args.argc > 2)
  { nSleep = atoi(command_args.argv[2]);
    assert(nSleep >= 0);
  }

  printf("Running %d Sleep(%d) tasks ...\n",num_points,nSleep);
  Rect<1> launch_bounds(Point<1>(0),Point<1>(num_points-1));
    Domain launch_domain = Domain::from_rect<1>(launch_bounds);
  ArgumentMap arg_map;
  for (int i = 0; i < num_points; i++)
  {
    int input = nSleep;
    arg_map.set_point(DomainPoint::from_point<1>(Point<1>(i)),
        TaskArgument(&input,sizeof(input)));
  }
  
  IndexLauncher index_launcher(HELLO_WORLD_INDEX_ID,launch_domain,TaskArgument(NULL, 0),arg_map);
  FutureMap fm = runtime->execute_index_space(ctx, index_launcher);
  fm.wait_all_results();

  clock_t endTime = clock();
  clock_t clockTicksTaken = endTime - startTime;
  double timeInSeconds = clockTicksTaken / (double) CLOCKS_PER_SEC;
  printf("Total Time: %f\n",timeInSeconds);
  
  for (int i = 0; i < num_points; i++)
  {
    double received = fm.get_result<double>(DomainPoint::from_point<1>(Point<1>(i)));
      printf("%f\n",received);
  }
}

double index_space_task(const Task *task,const std::vector<PhysicalRegion> &regions,Context ctx, HighLevelRuntime *runtime){

  clock_t startTime = clock();

  assert(task->local_arglen == sizeof(int));
  int input = *((const int*)task->local_args);

  usleep(input*1000);
  clock_t endTime = clock();
  clock_t clockTicksTaken = endTime - startTime;
  double timeInSeconds = clockTicksTaken / (double) CLOCKS_PER_SEC;

  return timeInSeconds;
}

int main(int argc, char **argv)
{
  HighLevelRuntime::set_top_level_task_id(TOP_LEVEL_TASK_ID);
  HighLevelRuntime::register_legion_task<top_level_task>(TOP_LEVEL_TASK_ID,Processor::LOC_PROC, true/*single*/, false/*index*/);
  HighLevelRuntime::register_legion_task<double,index_space_task>(HELLO_WORLD_INDEX_ID,Processor::LOC_PROC, false/*single*/, true/*index*/);

  return HighLevelRuntime::start(argc, argv);
}
