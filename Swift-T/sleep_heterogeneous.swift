import sys;
import io;
import stats;
import files;
import string;

(float d) timed_sleep(float s) {
  start = clock();
  void_r = sleep(s);
  wait(void_r) {
    d = clock()-start;
  }
}

main {
  argv_accept("f");
  string filepath = argv("f");
  string contents = read(input_file(filepath));
  string sleeps_str[] = split(contents, "\n");
  float jobs[];

  // Load the jobs from file
  N = size(sleeps_str)-1;
  foreach i in [0:N-1] {
    float sl_f = tofloat(sleeps_str[i])/1000;
    jobs[i] = sl_f;
  }

  // Execute the jobs
  float duration[];
  float cumul_start = clock();
  foreach j, index in jobs {
    duration[index] = timed_sleep(j);
  }
  // Print results
  wait (duration) {
    float cumul_duration = clock()-cumul_start =>
      float sum_duration = sum_float(duration) =>
      printf("%f, %f", cumul_duration, sum_duration);
  }
}
