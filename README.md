# console-wrapper-example
A wrapper for console-based applications to automate user input and read printed output

In some cases, it is necessary to send input to a console app which takes user input as an input,
and then receive the console output as a string which can be stored as a variable and used by the
wrapper. In other words, this allows Popen subprocesses to use readline() without hanging if there
isn't an expected number of output lines or a delimiter. Both files are meant to be used as an
example of this process so they are very basic.
