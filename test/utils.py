import re
import json

raw_data = """
{title: Blíže}
{author: Northpoint}
{key: B}

{comment: Verse}
Tvá [E]láska v[H]zala [H]m[Ahoj]i [B]dech  [B]
a změnila můj [C#m]svět,  
změnila můj [A]svět.

Jen [E]na tom záleží, [B]  
být s tebou na [C#m]vždy,  
být s tebou na [A]vždy.

{comment: Chorus}
[E]Pane vem mě k sobě [B]blíže,  
ve tvé blízkosti vždy [C#m]vím, že  
chci tebe poznat [A]víc,  
tebe poznat [E]víc.

[E]Tvoje láska smysl [B]dává  
a všechno překo [C#m]nává,  
já toužím poznat [A]víc,  
tebe poznat [E]víc.

[A]Ó, [E]ó, [B]tvoje láska [C#m]vznešená je,  
[A] Ó, [E]ó, [B]tvoje láska [C#m]láme.

[A][B][C]

word word word
"""

def parse_chordspro(text): 
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    metadata = dict(re.findall(r"{(\w+):\s*([^}]+)}", text.split("\n\n")[0]))

    sections_raw = re.split(r"\n{2,}", text.strip())
    sections = []

    def parse_line_to_segments(line):
        pattern = re.compile(r'\[([^\]]+)\]')
        segments = []
        last_pos = 0
        for match in pattern.finditer(line):
            start, end = match.span()
            chord = match.group(1)
            if start > last_pos:
                segments.append({"lyric": line[last_pos:start]})
            segments.append({"chord": chord})
            last_pos = end
        if last_pos < len(line):
            segments.append({"lyric": line[last_pos:]})
        return segments

    for block in sections_raw[1:]:  
        lines = block.strip().splitlines()
        section = {}
        if lines[0].startswith("{comment:"):
            section_name = re.match(r"{comment:\s*(.+?)}", lines[0]).group(1)
            section["comment"] = section_name
            lines = lines[1:]  
        section["lines"] = []
        for line in lines:
            if line.strip() == "":
                section["lines"].append([])  
            else:
                section["lines"].append(parse_line_to_segments(line))
        sections.append(section)

    song_data = {
        "metadata": metadata,
        "sections": sections
    }

    return json.dumps(song_data, ensure_ascii=False, indent=2)

print(parse_chordspro(raw_data))