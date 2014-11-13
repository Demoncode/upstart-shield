import errno
import os
import signal
import sys
import time


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s cmd arg1 arg2 ...\n"
                         % os.path.basename(sys.argv[0]))
        sys.exit(1)

    shield(*sys.argv[1:])


def shield(*args):
    pid = os.fork()

    if pid == 0:
        os.setpgrp()
        os.execlp(args[0], *args)
    else:
        def signal_handler(signum, frame):
            os.kill(pid, signum)

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        result = 0
        the_pid = 0

        while the_pid == 0:
            try:
                the_pid, result = os.waitpid(pid, 0)
            except OSError, e:
                if e.errno != errno.EINTR:
                    raise

        if os.WIFEXITED(result):
            sys.exit(os.WEXITSTATUS(result))
        else:
            sys.stderr.write("Shielded process (%s) was killed!\n" %
                             ' '.join(args))
            sys.exit(1)


def test_child_process():
    def signal_handler(signum, frame):
        sys.exit(123)

    signal.signal(signal.SIGUSR1, signal_handler)

    while True:
        time.sleep(1)


def test_master_process():
    child_pids = []

    print "Test master\nPID: %d\nPGID: %d" % (
        os.getpid(),
        os.getpgrp())

    for i in range(5):
        pid = os.fork()

        if pid == 0:
            test_child_process()
            sys.exit(0)
        else:
            child_pids.append(pid)
            print "Spawned child %d" % pid

    def signal_handler(signum, frame):
        print "Received signal %d, terminating cleanly" % signum

        for pid in child_pids:
            os.kill(pid, signal.SIGUSR1)

        error_count = 0

        while len(child_pids) > 0:
            for pid in list(child_pids):
                (the_pid, result) = os.waitpid(pid, os.WNOHANG)
                if the_pid != 0:
                    child_pids.remove(pid)
                    if (not os.WIFEXITED(result)
                            and os.WEXITSTATUS(result) != 123):
                        print "Process %d did not exit as expected" % pid
                        error_count += 1

        if error_count > 0:
            print ("Exiting after all children terminated (%d errors)"
                   % error_count)
        else:
            print "Exiting after all children terminated cleanly"
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        time.sleep(1)


def test_parent_process():
    args = dict(
        mypid=os.getpid(),
        mypgrp=os.getpgrp(),
    )

    print """\
Test parent
My PID: %(mypid)s
My PGID: %(mypgrp)s

Try the following:

    kill %(mypid)s\t\t- kill the individual process
    kill -TERM -%(mypgrp)s\t- kill the process group (like upstart)

Below this you will see a list of child process IDs. Kill one of those then
kill this one to see how it can go wrong.
""" % args

    shield('upstart-shield-test-master')
