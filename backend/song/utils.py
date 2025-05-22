import re

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

    return song_data