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
    for offset, opacity in [('0%', .32), ('45%', .10), ('78%', .045), ('100%', .18)]:
        node(shine, 'stop', offset=offset, stop_color='#e6f5ff', stop_opacity=opacity)
    # Keep the stronger motion in the free space around the fixed text. This
    # stationary mask softens bubbles as they pass through the reading area.
    visibility = node(defs, 'linearGradient', id='bubble-visibility', x1='0%', y1='0%', x2='0%' if mobile else '100%', y2='100%' if mobile else '0%')
    stops = ([('0%', 1), ('31%', 1), ('39%', .18), ('90%', .18), ('99%', 1), ('100%', 1)]
             if mobile else [('0%', 1), ('22%', 1), ('25%', .18), ('72%', .18), ('78%', 1), ('100%', 1)])
    for offset, opacity in stops:
        node(visibility, 'stop', offset=offset, stop_color='#ffffff', stop_opacity=opacity)
    readability = node(defs, 'mask', id='bubble-readability', maskUnits='userSpaceOnUse', x=0, y=0, width=width, height=height)
    node(readability, 'rect', width=width, height=height, fill='url(#bubble-visibility)')
    if mobile:
        edges = node(defs, 'linearGradient', id='bubble-edge-visibility')
        for offset, opacity in [('0%', 1), ('5%', 1), ('15%', 0), ('85%', 0), ('95%', 1), ('100%', 1)]:
            node(edges, 'stop', offset=offset, stop_color='#ffffff', stop_opacity=opacity)
        node(readability, 'rect', width=width, height=height, fill='url(#bubble-edge-visibility)')
    # Large bubbles drift independently; small ones share a narrow lane and
    # speed, with 0.38-second spacing so each group rises as a coherent chain.
    # Tuple: x, radius, duration, negative delay, horizontal drift, kind.
    large = (
        [(82, 27, 26, 20, -13), (142, 20, 22, 10, 10),
         (282, 24, 24, 13, 12), (320, 30, 28, 22, -14)]
        if mobile else
        [(82, 22, 22, 14, -12), (244, 30, 26, 17, -16),
         (650, 24, 23, 6, -16), (866, 22, 22, 12, 10),
         (912, 34, 27, 11, -15), (1005, 44, 30, 22, 18),
         (1050, 24, 24, 10, -12), (1125, 32, 28, 6, -16)]
    )
    bubbles = [(*item, 'large') for item in large]
    lanes = ([(19, 4.8, .6, 3), (371, 5.4, 2.8, -3)] if mobile else
             [(34, 4.4, .6, 3), (978, 4.8, 2.1, -3), (1152, 5.2, 3.4, 3)])
    for x, duration, phase, drift in lanes:
        for index, (radius, offset) in enumerate([(5, 0), (7, 2), (4, -1), (8, 1), (5.5, -2), (6.5, 0)]):
            delay = round((phase + index*.38) % duration, 2)
            bubbles.append((x+offset, radius, duration, delay, drift, 'stream'))
    rules = ['.bubble{opacity:.55;pointer-events:none}']
    layer = node(root, 'g', id='floating-bubbles', clip_path='url(#bubble-clip)', mask='url(#bubble-readability)', aria_hidden='true')
    for index, (x, radius, duration, delay, drift, kind) in enumerate(bubbles):
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
        bubble = node(layer, 'g', transform=f'translate({x} {still_y:g})', **{'class': f'bubble bubble-{index} bubble-{kind}'})
        if kind == 'stream' and animated:
            # Independent sideways oscillation keeps each fast chain organic.
            amplitude = (2.5 if mobile else 5) + (index % 3)
            period = 1.35 + (index % 5) * .19
            sway = f'bubble-sway-{index}'
            rules.append(f'.{sway}{{animation:{sway} {period:g}s ease-in-out -{index*.27:g}s infinite alternate}}')
            rules.append(f'@keyframes {sway}{{from{{transform:translateX(-{amplitude:g}px)}}to{{transform:translateX({amplitude:g}px)}}}}')
            bubble = node(bubble, 'g', **{'class': f'bubble-sway {sway}'})
        node(bubble, 'circle', r=radius, fill='url(#bubble-shine)', stroke='#d7efff', stroke_opacity=.6 if kind=='stream' else .48, stroke_width=.9 if kind=='stream' else 1.35)
        node(bubble, 'circle', cx=-radius*.35, cy=-radius*.38, r=max(.7 if kind=='stream' else 1.4, radius*.12), fill='#ffffff', fill_opacity=.34)
    rules.append('@media(prefers-reduced-motion:reduce){.bubble,.bubble-sway{animation:none!important;opacity:.4}}')
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
