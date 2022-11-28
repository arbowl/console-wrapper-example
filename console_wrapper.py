"""The purpose of this script is to provide a console app wrapper
and example test output. Normally readline() will hang if it's
expecting more output. If your console app doesn't have an EOL
delimiter and has a variable number of output lines, that can
cause readline() to hang forever. This puts readline() on a timer
so that the stream object will release its hold if no output is
received.
"""
import subprocess
from queue import Empty, Queue
from threading import Thread


class StreamReader:
    """The stream object which threads readline() and stops looking for
    stream output when the timeout argument is reached.
    """
    def __init__(self, stream):
        self.stream = stream
        self.queue = Queue()

        def enqueue(stream, queue):
            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    pass

        self.thread = Thread(
                target = enqueue,
                args = (self.stream, self.queue)
        )
        self.thread.daemon = True
        self.thread.start()

    def readline(self, timeout=None):
        try:
            return self.queue.get(
                    block = timeout is not None,
                    timeout = timeout
            )
        except Empty:
            return None


def start_console(program='python.exe', arg='-u', file='example_console_app.py'):
    """Opens a subprocess. If python, the -u argument will allow the wrapper to
    print line by line, rather than all at once when output stops.
    """
    return subprocess.Popen(
            [
                    program,
                    arg,
                    file
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
    )


def write(process, msg):
    """Writes a message to the console app which is interpreted as cin >> or input()
    """
    process.stdin.write((msg + '\n').encode())
    process.stdin.flush()


def terminate(process):
    """Closes the process
    """
    process.stdin.close()
    process.terminate()
    process.wait(timeout=0.2)


if __name__ == '__main__':
    process = start_console()
    reader = StreamReader(process.stdout)
    while not KeyboardInterrupt:
        msg = input('>>')
        write(process, msg)
        print('** BEGINNING OF CONSOLE OUTPUT **')
        while True:
            output = reader.readline(0.1)
            if not output:
                break
            if output:
                output = output.decode().strip()
                print(output)
                if ':' in output:
                    desired_output = output.split(':')[1]
        print('** END OF CONSOLE OUTPUT **')
        print('The test output was:' + desired_output)
    terminate(process)