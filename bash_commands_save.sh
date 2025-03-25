# Linux perf_event_open syscall available: Fail
# => solved by
sudo sh -c 'echo 2 >/proc/sys/kernel/perf_event_paranoid'

