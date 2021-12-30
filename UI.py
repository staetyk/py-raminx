from Pyraminx import run, show, solve
import Pyraminx
running = True
def stop():
    global running
    running = False
def test(step):
    show()
act = ""
while running == True:
    x = input()
    if x == "stop" or x == "solve" or x == "show":
        x += "()"
    elif x.startswith("."):
        x = "print(Pyraminx" + x + ")"
    elif x.startswith(","):
        x = "global act\nact = " + x.lstrip(",")
    else:
        x = "run(\"" + x + "\", {})".format(act)
    exec(x)