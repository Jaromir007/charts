from dataclasses import dataclass 
from typing import List, Optional, Dict 
import re

@dataclass
class Chord:
    chord: Optional[str]
    word: Optional[str]

@dataclass
class Wrapper: 
    parts: List[Chord]

@dataclass
class Line: 
    chords: List[Wrapper]

@dataclass
class Section: 
    name: Optional[str]
    lines: List[Line]

@dataclass 
class Chart: 
    title: str 
    meta: Dict[str, str]
    sections: List[Section]

RE_META = re.compile('\{(.+?)\}')
RE_CHORD = re.compile(r'\[([^\]]+)\]')

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

def split_word(text: str) -> List[str]:
    parts = []
    while text:
        match = RE_CHORD.search(text)
        if match:
            start, end = match.span()
            if start > 0:
                parts.append(text[:start])  
            parts.append(text[start:end])  
            text = text[end:]  
        else:
            parts.append(text)  
            break
    return parts


def has_chord(text: str) -> bool:
    return bool(RE_CHORD.search(text))

def is_chord_only(word: str) -> bool:
    return bool(RE_CHORD.fullmatch(word))

def parse_chordspro(chordspro: str) -> Chart:
    title = ""
    meta = {
        "key": None,
        "tempo": None,
        "author": None 
    }
    chart = Chart(title=title, meta=meta, sections=[])
    sections = get_sections(chordspro)
    for section in sections:
        section_temp = Section(name=None, lines=[])
        for line in section:     
            line_temp = Line(chords=[]) 
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
            else: 
                words = line.split()
                for word in words: 
                    if has_chord(word): 
                        if is_chord_only(word): 
                            chord = RE_CHORD.match(word).group(1)
                            line_temp.chords.append(Chord(chord=chord, word=None))
                        else:
                            pass
                    else: 
                        word = word.strip()
                        if word: 
                            line_temp.chords.append(Chord(chord=None, word=word))
                section_temp.lines.append(line_temp)
        chart.sections.append(section_temp)

    chart.title = title
    chart.meta = meta
    return chart


