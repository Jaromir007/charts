from dataclasses import dataclass 
from typing import List, Optional, Dict 
import re

@dataclass
class Token:
    chord: Optional[str]
    text: Optional[str]

@dataclass
class Line: 
    tokens: List[Token]

@dataclass
class Section: 
    name: Optional[str]
    lines: List[Line]

@dataclass 
class Chart: 
    title: str 
    meta: Dict[str, str]
    sections: List[Section]

def get_sections(chordspro): 
    sections = []
    section_temp = []
    for line in chordspro.splitlines():
        if line.strip() != "":
            section_temp.append(line)
        else: 
            sections.append(section_temp)
            section_temp = []
    if section_temp:
        sections.append(section_temp)

    return sections    

RE_META = re.compile('\{(.+?)\}')
RE_CHORD_WORD = re.compile(r'(?:\[([^\]]+)\]\s*)?([^\[\]\s]+)')

def parse_chordspro(chordspro: str) -> Chart:
    title = ""
    meta = {
        "key": None,
        "tempo": None,
        "author": None 
    }
    sections_list = []
    sections = get_sections(chordspro)
    for section in sections:
        section_struct = Section(None, [])
        for line in section:     
            line_struct = Line([])
            # Check if the line is meta info
            meta_match = RE_META.match(line)
            if meta_match: 
                content = meta_match.group(1).strip()
                if ':' in content: 
                    key, value = map(str.strip, content.split(':', 1))
                    key = key.lower()
                    if key == "title": 
                        title = value 
                    elif key in meta: 
                        meta[key] = value
            # if not, continue parsing
            else:
                for match in RE_CHORD_WORD.finditer(line):
                    chord, word = match.groups()
                    line_struct.tokens.append(Token(chord, word))

                if line_struct.tokens:
                    section_struct.lines.append(line_struct) 
        sections_list.append(section_struct)


    return Chart(title, meta, sections_list)

                    
