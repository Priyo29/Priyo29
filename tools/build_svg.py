"""Generate dark_mode.svg and light_mode.svg for the Priyo29 profile card.

Every panel row is padded with leading dots to a fixed WIDTH-column grid, so the
values line up in a column. Rows whose value is rewritten by today.py carry an
id on both the value and its dot run; today.py re-pads those at build time using
`justify_format(root, id, value, length)`, which always yields

    len(label) + 2 + length + 2

visible columns regardless of the value. The `length` numbers below are derived
from that identity, not guessed.
"""
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import asciify

WIDTH = 60          # panel columns
PANEL_X = 390
ART_X = 15
Y0, DY = 30, 20

DARK = dict(
    out="dark_mode.svg", bg="#161b22", fg="#c9d1d9", key="#ffa657",
    value="#a5d6ff", add="#3fb950", dele="#f85149", cc="#616e7f",
)
LIGHT = dict(
    out="light_mode.svg", bg="#f6f8fa", fg="#24292f", key="#953800",
    value="#0a3069", add="#1a7f37", dele="#cf222e", cc="#c2cfde",
)


def rule(title):
    """A section rule: title, then em-dashes out to WIDTH."""
    n = WIDTH - len(title) - 5
    return f"{escape(title)}</tspan> -{'—' * n}-—-"


def row(y, label, value, vid=None, length=None):
    """One `. Label: ..... value` line, dot-justified to WIDTH."""
    keyed = "".join(
        f'<tspan class="key">{escape(p)}</tspan>' if i % 2 == 0 else escape(p)
        for i, p in enumerate(_split(label))
    )
    if vid:
        # today.py owns the padding; it produces `length` + 2 columns of
        # (dots + value), so seed the file with the same geometry.
        pad = max(0, length - len(value))
        dots, did = "." * pad, f' id="{vid}_dots"'
        vattr = f' id="{vid}"'
    else:
        n = WIDTH - 4 - len(label) - 1 - len(value)
        if n < 0:
            # "." * -1 is "", which would silently drop the dot leader and push
            # this row's value past the shared right edge. Say so instead.
            print(f"warning: {label!r} row is {-n} column(s) over the "
                  f"{WIDTH}-col grid; value must be <= "
                  f"{WIDTH - 5 - len(label)} chars to keep the leader",
                  file=sys.stderr)
        dots = "." * max(0, n)
        did = vattr = ""
    return (
        f'<tspan x="{PANEL_X}" y="{y}" class="cc">. </tspan>{keyed}:'
        f'<tspan class="cc"{did}> {dots} </tspan>'
        f'<tspan class="value"{vattr}>{escape(value)}</tspan>'
    )


def _split(label):
    """'Languages.Programming' -> ['Languages', '.', 'Programming']"""
    out, parts = [], label.split(".")
    for i, p in enumerate(parts):
        if i:
            out.append(".")
        out.append(p)
    return out


def build(theme, art, panel):
    h = Y0 + DY * 24 + 20
    s = [
        "<?xml version='1.0' encoding='UTF-8'?>",
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'font-family="ConsolasFallback,Consolas,monospace" '
        f'width="985px" height="{h}px" font-size="16px">',
        "<style>",
        "@font-face {",
        "src: local('Consolas'), local('Consolas Bold');",
        "font-family: 'ConsolasFallback';",
        "font-display: swap;",
        "-webkit-size-adjust: 109%;",
        "size-adjust: 109%;",
        "}",
        f".key {{fill: {theme['key']};}}",
        f".value {{fill: {theme['value']};}}",
        f".addColor {{fill: {theme['add']};}}",
        f".delColor {{fill: {theme['dele']};}}",
        f".cc {{fill: {theme['cc']};}}",
        "text, tspan {white-space: pre;}",
        "</style>",
        f'<rect width="985px" height="{h}px" fill="{theme["bg"]}" rx="15"/>',
        f'<text x="{ART_X}" y="{Y0}" fill="{theme["fg"]}" class="ascii">',
    ]
    art_top = Y0 + DY * ((25 - len(art)) // 2)
    for i, line in enumerate(art):
        y = art_top + i * DY
        s.append(f'<tspan x="{ART_X}" y="{y}">{escape(line)}</tspan>')
    s.append("</text>")
    s.append(f'<text x="{PANEL_X}" y="{Y0}" fill="{theme["fg"]}">')
    s.extend(panel)
    s.append("</text>")
    s.append("</svg>")
    return "\n".join(s)


def panel_rows():
    y = iter(Y0 + DY * i for i in range(25))
    n = lambda: next(y)
    r = []
    r.append(f'<tspan x="{PANEL_X}" y="{n()}">{rule("priyabrata@mondal")}')
    r.append(row(n(), "OS", "macOS 26 (Tahoe), Debian Linux"))
    r.append(row(n(), "Uptime", "2 years, 10 months, 5 days", "age_data", 49))
    r.append(row(n(), "Host", "None, Inc."))
    r.append(row(n(), "Kernel", "Student (ETCE)"))
    r.append(row(n(), "IDE", "VSCode 1.114.0, Vim"))
    r.append(f'<tspan x="{PANEL_X}" y="{n()}" class="cc">. </tspan>')
    r.append(row(n(), "Languages.Programming", "C, C++, JavaScript, Python"))
    r.append(row(n(), "Languages.Computer", "HTML, CSS, JSON, Markdown"))
    r.append(row(n(), "Languages.Real", "English, Bengali, Hindi"))
    r.append(f'<tspan x="{PANEL_X}" y="{n()}" class="cc">. </tspan>')
    r.append(row(n(), "Hobbies.Software", "Systems Programming, Web Dev, Embedded C"))
    r.append(row(n(), "Hobbies.Hardware", "Arduino, Embedded Tinkering"))
    r.append(row(n(), "Hobbies.Others", "Competitive Programming, Maths"))
    r.append(f'<tspan x="{PANEL_X}" y="{n()}" class="cc">. </tspan>')
    r.append(f'<tspan x="{PANEL_X}" y="{n()}">{rule("- Contact")}')
    r.append(row(n(), "Email.Personal", "priyabratamondal1203@gmail.com"))
    r.append(row(n(), "GitHub", "Priyo29"))
    r.append(row(n(), "LinkedIn", "priyabrata-mondal29"))
    r.append(row(n(), "Discord", "priyo29"))
    r.append(f'<tspan x="{PANEL_X}" y="{n()}" class="cc">. </tspan>')
    r.append(f'<tspan x="{PANEL_X}" y="{n()}">{rule("- GitHub Stats")}')

    # two-column stat rows, padded by today.py via the ids below
    yr = n()
    r.append(
        f'<tspan x="{PANEL_X}" y="{yr}" class="cc">. </tspan>'
        '<tspan class="key">Repos</tspan>:'
        '<tspan class="cc" id="repo_data_dots"> ..... </tspan>'
        '<tspan class="value" id="repo_data">9</tspan>'
        ' {<tspan class="key">Contributed</tspan>:'
        '<tspan class="cc" id="contrib_data_dots"> .. </tspan>'
        '<tspan class="value" id="contrib_data">9</tspan>} | '
        '<tspan class="key">Stars</tspan>:'
        '<tspan class="cc" id="star_data_dots"> ............ </tspan>'
        '<tspan class="value" id="star_data">2</tspan>'
    )
    yr = n()
    r.append(
        f'<tspan x="{PANEL_X}" y="{yr}" class="cc">. </tspan>'
        '<tspan class="key">Commits</tspan>:'
        '<tspan class="cc" id="commit_data_dots"> ..................... </tspan>'
        '<tspan class="value" id="commit_data">0</tspan> | '
        '<tspan class="key">Followers</tspan>:'
        '<tspan class="cc" id="follower_data_dots"> .......... </tspan>'
        '<tspan class="value" id="follower_data">2</tspan>'
    )
    yr = n()
    r.append(
        f'<tspan x="{PANEL_X}" y="{yr}" class="cc">. </tspan>'
        '<tspan class="key">Lines of Code on GitHub</tspan>:'
        '<tspan class="cc" id="loc_data_dots">. </tspan>'
        '<tspan class="value" id="loc_data">0</tspan> ( '
        '<tspan class="addColor" id="loc_add">0</tspan>'
        '<tspan class="addColor">++</tspan>, '
        '<tspan id="loc_del_dots"> </tspan>'
        '<tspan class="delColor" id="loc_del">0</tspan>'
        '<tspan class="delColor">--</tspan> )'
    )
    return r


if __name__ == "__main__":
    out_dir = sys.argv[1]
    art = asciify.build(sys.argv[2], gamma=0.75, contrast=2.0, floor=0.10,
                        crop_top=0.12, bg_dot=".", bg_chroma=0.175)
    rows = panel_rows()
    for theme in (DARK, LIGHT):
        with open(f"{out_dir}/{theme['out']}", "w", encoding="utf-8") as f:
            f.write(build(theme, art, rows) + "\n")
        print("wrote", theme["out"])
