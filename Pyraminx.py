from ansi_escape_room.colored import fg, attr


pyramid = {
    "tip" : {
        "U" : 0,
        "L" : 0,
        "R" : 0,
        "B" : 0
    },
    "quad" : {
        "U" : 0,
        "L" : 0,
        "R" : 0,
        "B" : 0
    },
    "side" : {
        "U" : {
            "L" : "u",
            "R" : "u",
            "B" : "u"
        },
        "L" : {
            "U" : "l",
            "R" : "l",
            "B" : "l"
        },
        "R" : {
            "U" : "r",
            "L" : "r",
            "B" : "r"
        },
        "B" : {
            "U" : "b",
            "L" : "b",
            "R" : "b"
        }
    }
}


def low(tip: str, clock: bool):
    pyramid["tip"][tip] += 1 if clock else 2
    pyramid["tip"][tip] %= 3

def High(quad: str, side: str):
    low(quad, False)

    pyramid["quad"][quad] -= 1
    pyramid["quad"][quad] %= 3

    og = [
        str(pyramid["side"][side[0]][side[2]]),
        str(pyramid["side"][side[0]][side[1]]),
        str(pyramid["side"][side[1]][side[0]]),
        str(pyramid["side"][side[1]][side[2]]),
        str(pyramid["side"][side[2]][side[1]]),
        str(pyramid["side"][side[2]][side[0]])
    ]
    og = tuple(og[2:]+og[:2])

    pyramid["side"][side[0]][side[2]], pyramid["side"][side[0]][side[1]], pyramid["side"][side[1]][side[0]], pyramid["side"][side[1]][side[2]], pyramid["side"][side[2]][side[1]], pyramid["side"][side[2]][side[0]] = og

def high(quad: str, clock: bool, side: str):
    for _ in range(2 if clock else 1):
        High(quad, side)


moves = {
    "u" : "low('B', True)",
    "u'" : "low('B', False)",
    "U" : "high('B', True, 'ULR')",
    "U'" : "high('B', False, 'ULR')",
    "l" : "low('R', True)",
    "l'" : "low('R', False)",
    "L" : "high('R', True, 'UBL')",
    "L'" : "high('R', False, 'UBL')",
    "r" : "low('L', False)",
    "r'" : "low('L', True)",
    "R" : "high('L', False, 'URB')",
    "R'" : "high('L', True, 'URB')",
    "b" : "low('U', False)",
    "b'" : "low('U', True)",
    "B" : "high('U', False, 'BRL')",
    "B'" : "high('U', True, 'BRL')"
}


rotation = "UU"


rot = {
    "UU" : {
        "U" : "U",
        "L" : "L",
        "R" : "R",
        "B" : "B"
    },
    "UL" : {
        "U" : "U",
        "L" : "B'",
        "R" : "L'",
        "B" : "R"
    },
    "UR" : {
        "U" : "U",
        "L" : "R'",
        "R" : "B",
        "B" : "L'"
    },
    "LU" : {
        "U" : "L",
        "L" : "R'",
        "R" : "U'",
        "B" : "B"
    },
    "LL" : {
        "U" : "L",
        "L" : "U",
        "R" : "B",
        "B" : "R"
    },
    "LB" : {
        "U" : "L",
        "L" : "B'",
        "R" : "R",
        "B" : "U'"
    },
    "RU" : {
        "U" : "R'",
        "L" : "U",
        "R" : "L'",
        "B" : "B"
    },
    "RR" : {
        "U" : "R'",
        "L" : "B'",
        "R" : "U'",
        "B" : "L'"
    },
    "RB" : {
        "U" : "R'",
        "L" : "L",
        "R" : "B",
        "B" : "U'"
    },
    "BL" : {
        "U" : "B'",
        "L" : "L",
        "R" : "U'",
        "B" : "R"
    },
    "BR" : {
        "U" : "B'",
        "L" : "U",
        "R" : "R",
        "B" : "L'"
    },
    "BB" : {
        "U" : "B'",
        "L" : "R'",
        "R" : "L'",
        "B" : "U'"
    }
}


def moving(x: str):
    case = x.isupper()
    x = x.upper()
    tag = "'" in x
    x = x.replace("'","")

    y = str(rot[rotation][x])

    if not case:
        y = y.lower()
    if tag:
        y += "'"
        y = y.replace("''","")
    
    return str(moves[y])


def rotate(pers: str):
    global rotation
    pers = pers.upper()
    new = str(rot[rotation][pers[0]]).replace("'","")
    opposites = {
        "U" : "B",
        "L" : "R",
        "R" : "L",
        "B" : "U"
    }
    face = str(rot[rotation][opposites[pers[1]]]).replace("'","")
    new += opposites[face]
    rotation = new



algorithm = {}

def N_slash_A(step: str):
    pass

def run(sequence: str, action = N_slash_A):
    sequence = sequence.splitlines()
    for seq in sequence:
        if seq == "":
            continue
        elif "=" in seq:
            seq = seq.split("=")
            algorithm[seq[0]] = seq[1]
        else:
            seq = seq.split("-")
            for step in seq:
                if len(step) > 2 and step.isalpha():
                    run(algorithm[step])
                elif len(step) == 2 and step.isalpha():
                    if step.isupper():
                        global rotation
                        rotation = step
                    elif step.islower():
                        rotate(step)
                else:
                    exec(moving(step))
                    action(step)


def solve():
    pos = {
        "tip" : {
            "U" : 0,
            "L" : 0,
            "R" : 0,
            "B" : 0
        },
        "quad" : {
            "U" : 0,
            "L" : 0,
            "R" : 0,
            "B" : 0
        },
        "side" : {
            "U" : {
                "L" : "u",
                "R" : "u",
                "B" : "u"
            },
            "L" : {
                "U" : "l",
                "R" : "l",
                "B" : "l"
            },
            "R" : {
                "U" : "r",
                "L" : "r",
                "B" : "r"
            },
            "B" : {
                "U" : "b",
                "L" : "b",
                "R" : "b"
            }
        }
    }

    pyramid.update(pos)

    rotation = "UU"


def show():
    layout = """\n{0}{1}{2}{3}{4}     {6}{7}{8}{9}{10}
 {11}{12}{13}   {5}   {17}{18}{19}
  {20}   {14}{15}{16}   {26}
     {21}{22}{23}{24}{25}

     {27}{28}{29}{30}{31}
      {32}{33}{34}
       {35}    
    """

    tri = [
        "lrb"[pyramid["tip"]["U"]],
        "lrb"[pyramid["quad"]["U"]],
        pyramid["side"]["L"]["R"],
        "lur"[pyramid["quad"]["B"]],
        "lur"[pyramid["tip"]["B"]],
        "url"[pyramid["tip"]["B"]],
        "rlu"[pyramid["tip"]["B"]],
        "rlu"[pyramid["quad"]["B"]],
        pyramid["side"]["R"]["L"],
        "rbl"[pyramid["quad"]["U"]],
        "rbl"[pyramid["tip"]["U"]],
        pyramid["side"]["L"]["B"],
        "lbu"[pyramid["quad"]["R"]],
        pyramid["side"]["L"]["U"],
        pyramid["side"]["U"]["L"],
        "url"[pyramid["quad"]["B"]],
        pyramid["side"]["U"]["R"],
        pyramid["side"]["R"]["U"],
        "rub"[pyramid["quad"]["L"]],
        pyramid["side"]["R"]["B"],
        "lbu"[pyramid["tip"]["R"]],
        "ulb"[pyramid["tip"]["R"]],
        "ulb"[pyramid["quad"]["R"]],
        pyramid["side"]["U"]["B"],
        "ubr"[pyramid["quad"]["L"]],
        "ubr"[pyramid["tip"]["L"]],
        "rub"[pyramid["tip"]["L"]],
        "bul"[pyramid["tip"]["R"]],
        "bul"[pyramid["quad"]["R"]],
        pyramid["side"]["B"]["U"],
        "bru"[pyramid["quad"]["L"]],
        "bru"[pyramid["tip"]["L"]],
        pyramid["side"]["B"]["L"],
        "blr"[pyramid["quad"]["U"]],
        pyramid["side"]["B"]["R"],
        "blr"[pyramid["tip"]["U"]]
    ]

    u = chr(int("25b2",16))
    d = chr(int("25bc",16))

    point = [d,u,d,u,d,u,d,u,d,u,d,d,u,d,u,d,u,d,u,d,d,u,d,u,d,u,d,d,u,d,u,d,d,u,d,d]

    angles = []
    i = 0
    for x in tri:
        if x == "u":
            txt = fg(25)
        elif x == "l":
            txt = fg(2)
        elif x == "r":
            txt = fg(1)
        else:
            txt = fg(11)
        txt += point[i]

        txt += attr(0)

        angles.append(txt)

        i += 1

    triangles = tuple(angles)
    print(layout.format(*triangles))

