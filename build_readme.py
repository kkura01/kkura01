from pathlib import Path
from xml.sax.saxutils import escape

# Visual column width of the spec lines (matches andrew@grant card).
COL = 62


def dotted(label: str, value: str) -> tuple[str, str]:
    """Return (dot_string, value) so label + dots + value line up."""
    prefix = f". {label}:"
    # " {dots} " around the filler
    fill = COL - len(prefix) - len(value) - 2
    if fill < 1:
        dots = "."
    else:
        dots = "." * fill
    return f" {dots} ", value


def tspan(y, inner, x=390):
    return f'<tspan x="{x}" y="{y}">{inner}</tspan>'


def spec(y, label, value, key_parts=None):
    dots, val = dotted(label, value)
    if key_parts is None:
        keys = "".join(f'<tspan class="key">{escape(p)}</tspan>' for p in [label])
    else:
        keys = '<tspan class="key">' + '</tspan>.<tspan class="key">'.join(
            escape(p) for p in key_parts
        ) + "</tspan>"
        # dotted() used full "Languages.Programming" as label, keys render with a dot between
    return (
        f'<tspan x="390" y="{y}" class="cc">. </tspan>'
        f"{keys}:<tspan class=\"cc\">{escape(dots)}</tspan>"
        f'<tspan class="value">{escape(val)}</tspan>'
    )


def spec_nested(y, left, right, value):
    label = f"{left}.{right}"
    dots, val = dotted(label, value)
    return (
        f'<tspan x="390" y="{y}" class="cc">. </tspan>'
        f'<tspan class="key">{escape(left)}</tspan>.'
        f'<tspan class="key">{escape(right)}</tspan>:'
        f'<tspan class="cc">{escape(dots)}</tspan>'
        f'<tspan class="value">{escape(val)}</tspan>'
    )


def blank_ascii():
    # 25 rows, same y-step as the original portrait; spaces hold the left column.
    lines = []
    for i in range(25):
        y = 30 + i * 20
        lines.append(f'<tspan x="15" y="{y}">                                            </tspan>')
    return "\n".join(lines)


def stats_block():
    # Keep the same three-line GitHub Stats layout and ids.
    repo, contrib, stars = "5", "6", "0"
    commits, followers = "75", "1"
    loc, loc_add, loc_del = "—", "—", "—"

    def pad_dots(label, value, width):
        fill = max(1, width - len(str(value)))
        return " " + ("." * fill) + " "

    return f"""<tspan x="390" y="450">- GitHub Stats</tspan> -—————————————————————————————————————————-—-
<tspan x="390" y="470" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots">{escape(pad_dots("Repos", repo, 4))}</tspan><tspan class="value" id="repo_data">{repo}</tspan> {{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">{contrib}</tspan>}} | <tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots">{escape(pad_dots("Stars", stars, 11))}</tspan><tspan class="value" id="star_data">{stars}</tspan>
<tspan x="390" y="490" class="cc">. </tspan><tspan class="key">Commmits</tspan>:<tspan class="cc" id="commit_data_dots">{escape(pad_dots("Commmits", commits, 17))}</tspan><tspan class="value" id="commit_data">{commits}</tspan> | <tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots">{escape(pad_dots("Followers", followers, 7))}</tspan><tspan class="value" id="follower_data">{followers}</tspan>
<tspan x="390" y="510" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc" id="loc_data_dots">. </tspan><tspan class="value" id="loc_data">{loc}</tspan> ( <tspan class="addColor" id="loc_add">{loc_add}</tspan><tspan class="addColor">++</tspan>, <tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">{loc_del}</tspan><tspan class="delColor">--</tspan> )"""


def body_text(fill):
    return f"""<text x="390" y="30" fill="{fill}">
<tspan x="390" y="30">dhruv@kkura</tspan> -———————————————————————————————————————————-—-
{spec(50, "OS", "Windows 11")}
{spec(70, "Uptime", "5 years, 6 months, 30 days")}
{spec(90, "Host", "Personal Workstation")}
{spec(110, "Kernel", "Software Developer")}
{spec(130, "IDE", "Cursor, VS Code")}
<tspan x="390" y="150" class="cc">. </tspan>
{spec_nested(170, "Languages", "Programming", "Python, JavaScript", "C++", "Typecript", "C")}
{spec_nested(190, "Languages", "Computer", "HTML, CSS, JSON, Jupyter, YAML")}
{spec_nested(210, "Languages", "Real", "English, Hindi")}
<tspan x="390" y="230" class="cc">. </tspan>
{spec_nested(250, "Hobbies", "Software", "Machine Learning, Voice Apps")}
{spec_nested(270, "Hobbies", "Hardware", "PCs, Custom Setups")}
<tspan x="390" y="310">- Contact</tspan> -——————————————————————————————————————————————-—-
# {spec_nested(330, "Email", "Personal", "github.com/kkura01")}
{spec_nested(350, "Email", "Personal", "dhruvwange07@gmail.com")}
{spec_nested(370, "Email", "Work", "dhruv.devxz@gmail.com")}
{spec(390, "LinkedIn", "Dhruv Wange")}
{spec(410, "Discord", "skiiiii")}
{stats_block()}
</text>"""


def svg(mode: str) -> str:
    if mode == "dark":
        style = """.key {fill: #ffa657;}
.value {fill: #a5d6ff;}
.addColor {fill: #3fb950;}
.delColor {fill: #f85149;}
.cc {fill: #616e7f;}
text, tspan {white-space: pre;}"""
        bg, ascii_fill, text_fill = "#161b22", "#c9d1d9", "#c9d1d9"
    else:
        style = """.key {fill: #953800;}
.value {fill: #0a3069;}
.addColor {fill: #1a7f37;}
.delColor {fill: #cf222e;}
.cc {fill: #c2cfde;}
text, tspan {white-space: pre;}"""
        bg, ascii_fill, text_fill = "#f6f8fa", "#24292f", "#24292f"

    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
{style}
</style>
<rect width="985px" height="530px" fill="{bg}" rx="15"/>
<text x="15" y="30" fill="{ascii_fill}" class="ascii">
{blank_ascii()}
</text>
{body_text(text_fill)}
</svg>
"""


root = Path(r"C:\Users\Dhruv\Desktop\prof")
(root / "dark_mode.svg").write_text(svg("dark"), encoding="utf-8")
(root / "light_mode.svg").write_text(svg("light"), encoding="utf-8")
print("wrote svgs")
