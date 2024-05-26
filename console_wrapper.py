"""The purpose of this script is to provide a console app wrapper
and example test output. Normally readline() will hang if it's
expecting more output. If your console app doesn't have an EOL
delimiter and has a variable number of output lines, that can
cause readline() to hang forever. This puts readline() on a timer
so that the stream object will release its hold if no output is
received.
"""

from __future__ import annotations

from subprocess import Popen, STARTUPINFO, STARTF_USESHOWWINDOW, PIPE
from queue import Empty, Queue
from threading import Thread
from typing import Any, Optional


class ConsoleWrapper:
    """The stream object which threads readline() and stops looking for
    stream output when the timeout argument is reached.
    """
    def __init__(self,args: list[str]) -> None:
        startupinfo = STARTUPINFO()
        startupinfo.dwFlags |= STARTF_USESHOWWINDOW
        self.process = Popen(
            args,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            start_new_session=True,
            startupinfo=startupinfo,
        )
        self.queue: Queue = Queue()
        self.thread = Thread(target=self._enqueue)
        self.thread.daemon = True
        self.thread.start()

    def __enter__(self) -> ConsoleWrapper:
        """Enter context manager"""
        return self

    def __exit__(self, *args, **kwargs) -> None:
        """Exit context manager"""
        self.close()

    def _enqueue(self) -> None:
        """Adds output from the console to the queue"""
        while True:
            if self.process.stdout is None:
                return
            line = self.process.stdout.readline()
            if line:
                self.queue.put(line.decode().strip())

    def readline(self, timeout: float = 1.0) -> Optional[str]:
        """Returns a line of output from the process"""
        try:
            return self.queue.get(block=True, timeout=timeout)
        except Empty:
            return None

    def write(self, msg: Any) -> None:
        """Writes a message to the console app which is interpreted as cin >> or
        input()
        """
        if self.process is None or self.process.stdin is None:
            return
        self.process.stdin.write(f"{msg}\r\n".encode())
        self.process.stdin.flush()

    def close(self) -> None:
        """Closes the process
        """
        if self.process is None or self.process.stdin is None:
            return
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait(timeout=0.2)


if __name__ == '__main__':
    # Usage example
    with ConsoleWrapper(["python.exe", "-u", "example_console_app.py"]) as wrapper:
        wrapper.write("Looking for: 3")
        while (output := wrapper.readline(1)) is not None:
            print(output)
            if "3" in output:
                print(f'Found "3" in string "{output}"')
                break
        if output is None:
            print('"3" was not found in output')
        input()
