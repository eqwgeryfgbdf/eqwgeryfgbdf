"""Build self-contained SVG profile cards with the Python standard library.

Text, card geometry, icons, and official university marks remain vectors.
Only the existing account portrait is embedded as its original PNG.
"""
from pathlib import Path
import base64
import copy
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/profile'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,'Microsoft JhengHei',sans-serif"
AVATAR = 'data:image/png;base64,' + base64.b64encode((OUT / 'source/avatar.png').read_bytes()).decode('ascii')
PALETTES = {
    'light': dict(canvas='#ffffff', surface='#f5f7fb', border='#dce6f5', blue='#0071e3', muted='#6e6e73', text='#1d1d1f'),
    'dark': dict(canvas='#0d1117', surface='#161b22', border='#303b4b', blue='#8abdff', muted='#a6b0bd', text='#f0f3f6'),
}


def node(parent, tag, **attrs):
    return ET.SubElement(parent, '{' + NS + '}' + tag, {k.replace('_', '-'): str(v) for k, v in attrs.items()})


def text(parent, value, x, y, size, fill, weight=400, anchor='start', **attrs):
    element = node(parent, 'text', x=x, y=y, font_size=size, fill=fill, font_weight=weight, text_anchor=anchor, **attrs)
    element.text = value
    return element


def canvas(width, height, title, description, palette):
    root = ET.Element('{' + NS + '}svg', {'width': str(width), 'height': str(height), 'viewBox': f'0 0 {width} {height}', 'role': 'img', 'aria-labelledby': 'title description', 'font-family': FONT})
    node(root, 'title', id='title').text = title
    node(root, 'desc', id='description').text = description
    node(root, 'rect', width=width, height=height, fill=palette['canvas'])
    return root


def icon(parent, name, x, y, size, fill):
    source = ET.parse(OUT / 'source/icons' / (name + '.svg')).getroot()
    _, _, width, height = map(float, source.attrib['viewBox'].split())
    scale = size / max(width, height)
    group = node(parent, 'g', transform=f'translate({x + (size - width * scale) / 2:g} {y + (size - height * scale) / 2:g}) scale({scale:g})', fill=fill)
    for child in source:
        group.append(copy.deepcopy(child))


def school_mark(parent, name, cx, cy, radius, palette):
    # White backing preserves the universities' official colors in either theme.
    node(parent, 'circle', cx=cx, cy=cy, r=radius, fill='#ffffff', stroke='#c6dafa', stroke_width=1.5)
    source = ET.parse(OUT / 'source/schools' / (name + '.svg')).getroot()
    _, _, width, height = map(float, source.attrib['viewBox'].split())
    maximum = radius * 1.58
    scale = maximum / max(width, height)
    source.attrib.update(x=f'{cx - width * scale / 2:g}', y=f'{cy - height * scale / 2:g}', width=f'{width * scale:g}', height=f'{height * scale:g}')
    # Independent marks can contain the same PDF-generated clip IDs.
    for element in source.iter():
        if 'id' in element.attrib:
            element.attrib['id'] = name + '-' + element.attrib['id']
        for key, value in list(element.attrib.items()):
            element.attrib[key] = value.replace('url(#', 'url(#' + name + '-')
            if key.endswith('href') and value.startswith('#'):
                element.attrib[key] = '#' + name + '-' + value[1:]
    parent.append(source)


def floating_bubbles(root, width, height, pad, mobile, animated=True):
    """Decorative CSS-only animation; clipped behind the fixed profile content."""
    defs = node(root, 'defs')
    clip = node(defs, 'clipPath', id='bubble-clip')
    node(clip, 'rect', x=pad, y=pad, width=width-2*pad, height=height-2*pad, rx=26 if mobile else 30)
    shine = node(defs, 'radialGradient', id='bubble-shine', cx='28%', cy='24%', r='76%')
    for offset, opacity in [('0%', .20), ('45%', .055), ('78%', .025), ('100%', .11)]:
        node(shine, 'stop', offset=offset, stop_color='#e6f5ff', stop_opacity=opacity)
    # x, radius, duration, negative delay, horizontal drift. Fixed values make
    # generation reproducible and keep loops out of phase without JavaScript.
    bubbles = (
        [(36, 13, 23, 4, 9), (84, 24, 29, 19, -12), (134, 9, 25, 8, 10),
         (240, 12, 26, 17, -9), (303, 25, 31, 12, 12), (351, 16, 24, 21, -10)]
        if mobile else
        [(46, 14, 24, 5, 10), (244, 26, 30, 19, -13), (430, 12, 25, 3, 12),
         (650, 20, 29, 13, -12), (842, 14, 23, 7, 10), (946, 42, 32, 16, -16),
         (1055, 26, 28, 24, 15), (1144, 18, 24, 10, -13), (1010, 10, 22, 4, 8)]
    )
    rules = ['.bubble{opacity:.55;pointer-events:none}']
    layer = node(root, 'g', id='floating-bubbles', clip_path='url(#bubble-clip)', aria_hidden='true')
    for index, (x, radius, duration, delay, drift) in enumerate(bubbles):
        bottom, top = height + radius + 4, -radius - 4
        still_y = bottom + (top-bottom) * delay/duration
        name = f'bubble-rise-{index}'
        if animated:
            rules.append(f'.bubble-{index}{{animation:{name} {duration}s linear -{delay}s infinite}}')
            rules.append(
                f'@keyframes {name}{{'
                f'0%{{transform:translate({x}px,{bottom}px);opacity:0}}'
                '10%{opacity:.8}'
                f'50%{{transform:translate({x+drift}px,{height/2:g}px);opacity:1}}'
                '90%{opacity:.8}'
                f'100%{{transform:translate({x+drift*.3:g}px,{top}px);opacity:0}}'
                '}'
            )
        bubble = node(layer, 'g', transform=f'translate({x} {still_y:g})', **{'class': f'bubble bubble-{index}'})
        node(bubble, 'circle', r=radius, fill='url(#bubble-shine)', stroke='#d7efff', stroke_opacity=.28, stroke_width=1.1)
        node(bubble, 'circle', cx=-radius*.35, cy=-radius*.38, r=max(1.4, radius*.12), fill='#ffffff', fill_opacity=.22)
    rules.append('@media(prefers-reduced-motion:reduce){.bubble{animation:none!important;opacity:.4}}')
    node(root, 'style').text = '\n'.join(rules)


def hero(palette, mobile=False, animated=True):
    width, height = (390, 422) if mobile else (1200, 320)
    root = canvas(width, height, 'Lung Yu-Cheng · 龍禹丞', "Researcher, Inventor, Engineer. Master's student in Artificial Intelligence Technology at National Taipei University of Technology.", palette)
    pad = 5 if mobile else 8
    node(root, 'rect', x=pad, y=pad, width=width-2*pad, height=height-2*pad, rx=26 if mobile else 30, fill='#0062d6')
    floating_bubbles(root, width, height, pad, mobile, animated)
    cx, cy, radius = (195, 85, 54.5) if mobile else (153, 160, 90.5)
    clip = node(node(root, 'defs'), 'clipPath', id='portrait-clip')
    node(clip, 'circle', cx=cx, cy=cy, r=radius)
    node(root, 'image', x=cx-radius, y=cy-radius, width=radius*2, height=radius*2, href=AVATAR, preserveAspectRatio='xMidYMid slice', clip_path='url(#portrait-clip)')
    node(root, 'circle', cx=cx, cy=cy, r=radius, fill='none', stroke='#b9dbff', stroke_width=3 if mobile else 5)
    if mobile:
        text(root, 'RESEARCHER · INVENTOR · ENGINEER', 195, 171, 11, '#c7e2ff', 600, 'middle', letter_spacing=1.6)
        text(root, 'Lung Yu-Cheng', 195, 214, 32, '#ffffff', 700, 'middle', letter_spacing=-1)
        text(root, '龍禹丞', 195, 247, 24, '#c7e2ff', 500, 'middle', lang='zh-Hant')
        for line, y in [('Master’s student · Artificial Intelligence', 282), ('Technology', 304), ('National Taipei University of Technology', 327)]:
            text(root, line, 195, y, 15, '#ffffff', 500, 'middle')
        text(root, 'Computer Vision · Multimodal AI · Embedded Systems', 195, 363, 13, '#e2f0ff', anchor='middle')
    else:
        text(root, 'RESEARCHER · INVENTOR · ENGINEER', 290, 69, 16, '#c7e2ff', 600, letter_spacing=2)
        text(root, 'Lung Yu-Cheng', 290, 137, 54, '#ffffff', 700, letter_spacing=-1.5)
        text(root, '龍禹丞', 685, 137, 37, '#c7e2ff', 500, lang='zh-Hant')
        text(root, 'Master’s student · Artificial Intelligence Technology', 290, 186, 22, '#ffffff', 500)
        text(root, 'National Taipei University of Technology', 290, 219, 22, '#ffffff', 500)
        text(root, 'Computer Vision · Multimodal AI · Embedded Systems', 290, 264, 19, '#e2f0ff')
    return root


def education(palette, mobile=False):
    width, height = (390, 480) if mobile else (1200, 326)
    root = canvas(width, height, 'Education · 學歷', 'Official Taipei Tech and Lunghwa University marks. Master’s student in Artificial Intelligence Technology; B.S. in Computer Information and Network Engineering, 2022–2026.', palette)
    pad = 5 if mobile else 8
    node(root, 'rect', x=pad, y=pad, width=width-2*pad, height=height-2*pad, rx=24 if mobile else 28, fill=palette['surface'], stroke=palette['border'], stroke_width=2)
    if mobile:
        school_mark(root, 'ntut', 62, 56, 32, palette)
        school_mark(root, 'lhu', 62, 266, 32, palette)
        for value, y in [('National Taipei University of', 116), ('Technology', 142), ('Lunghwa University of Science', 326), ('and Technology', 352)]:
            text(root, value, 27, y, 21, palette['text'], 650, letter_spacing=-.3)
        for value, y in [('Artificial Intelligence Technology', 171), ('B.S. in Computer Information and', 382), ('Network Engineering', 404)]:
            text(root, value, 27, y, 15, palette['muted'])
        for value, y in [('MASTER’S STUDENT', 195), ('2022–2026 · IoT Technical Excellence', 432), ('Program', 452)]:
            text(root, value, 27, y, 13, palette['blue'], 600)
        node(root, 'path', d='M27 219H363', stroke=palette['border'], fill='none')
    else:
        school_mark(root, 'ntut', 94, 98, 46, palette)
        school_mark(root, 'lhu', 94, 233, 46, palette)
        for value, y in [('National Taipei University of Technology', 82), ('Lunghwa University of Science and Technology', 217)]:
            text(root, value, 164, y, 29, palette['text'], 650, letter_spacing=-.5)
        for value, y in [('Artificial Intelligence Technology', 117), ('B.S. in Computer Information and Network Engineering', 252)]:
            text(root, value, 164, y, 21, palette['muted'])
        for value, y in [('MASTER’S STUDENT', 144), ('2022–2026 · IoT Technical Excellence Program', 279)]:
            text(root, value, 164, y, 16, palette['blue'], 600)
        node(root, 'path', d='M46 165H1154', stroke=palette['border'], fill='none')
    return root


BUTTONS = {'website': ('Website', 'globe', 240, 99), 'cv': ('CV', 'file-lines', 160, 35), 'scholar': ('Scholar', 'graduation-cap', 240, 97), 'linkedin': ('LinkedIn', 'linkedin-in', 260, 107), 'email': ('Email', 'envelope', 210, 68)}


def button(name, palette, dark):
    label, mark, width, text_width = BUTTONS[name]
    root = canvas(width, 80, label, label + ' profile link', palette)
    node(root, 'rect', x=5, y=5, width=width-10, height=70, rx=35, fill='#17263b' if dark else '#f5f9ff', stroke='#334f74' if dark else '#c6dbf8', stroke_width=2)
    x = (width - 27 - 13 - text_width) / 2
    color = '#8abdff' if dark else '#0067d8'
    icon(root, mark, x, 26.5, 27, color)
    text(root, label, x+40, 49.5, 27, color, 550, letter_spacing=.2)
    return root


def main():
    written = []
    for theme, palette in PALETTES.items():
        for name, render in [('hero', hero), ('education', education)]:
            for mobile in [False, True]:
                filename = f'{name}{"-mobile" if mobile else ""}-{theme}.svg'
                ET.ElementTree(render(palette, mobile)).write(OUT / filename, encoding='utf-8', xml_declaration=True)
                written.append(filename)
                if name == 'hero':
                    filename = f'hero-still{"-mobile" if mobile else ""}-{theme}.svg'
                    ET.ElementTree(hero(palette, mobile, animated=False)).write(OUT / filename, encoding='utf-8', xml_declaration=True)
                    written.append(filename)
        for name in BUTTONS:
            filename = f'{name}-{theme}.svg'
            ET.ElementTree(button(name, palette, theme=='dark')).write(OUT / filename, encoding='utf-8', xml_declaration=True)
            written.append(filename)
    print(f'Generated {len(written)} SVG cards.')


if __name__ == '__main__':
    main()
