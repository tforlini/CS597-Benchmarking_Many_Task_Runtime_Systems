import sys;
import io;
import stats;

(float d) timed_sleep(float s) {
  start = clock();
  void_r = sleep(s);
  wait(void_r) {
    d = clock()-start;
  }
}

main {
  argv_accept("n", "t");
  int N = toint(argv("n", "1000"));
  float s = tofloat(argv("t", "0"));
  float duration[];
  float cumul_start = clock();
  foreach i in [0:N-1] {
    duration[i] = timed_sleep(s);
  }
  // Print results
  wait (duration) {
    float cumul_duration = clock()-cumul_start =>
      float sum_duration = sum_float(duration) =>
      printf("%f, %f", cumul_duration, sum_duration);
  }
}
