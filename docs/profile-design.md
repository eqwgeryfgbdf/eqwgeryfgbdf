# Vector profile presentation assets

The README uses native Markdown for content and links, with self-contained SVG cards for the rounded layout that GitHub cannot style directly. Text, geometry, icons, and the official university marks are vector elements. The account portrait is the only embedded raster image; its original PNG is preserved.

Regenerate all 22 cards (including four still hero variants) with the Python standard library:

```sh
python scripts/generate-profile-svg.py
```

Serve the repository over HTTP and open `docs/profile-cards.html?asset=hero`. Add `&theme=dark` for dark mode or `&mobile=1` for the mobile hero and education cards. Available assets: hero, education, website, cv, scholar, linkedin, email.

| Asset | Desktop viewBox | Mobile viewBox |
| --- | --- | --- |
| hero | 1200 × 320 | 390 × 422 |
| education | 1200 × 326 | 390 × 480 |
| website / scholar | 240 × 80 | same |
| cv | 160 × 80 | same |
| linkedin | 260 × 80 | same |
| email | 210 × 80 | same |

Files use `assets/profile/{asset}[-mobile]-{light|dark}.svg`. Buttons display at half their nominal size. Responsive picture sources choose the correct card. SVG text remains editable; no screenshots, HTML foreignObject, scripts, remote fonts, or external image requests are embedded. README alternative text and an expandable education transcript preserve readable content.

The hero includes two distinct bubble motions behind its stationary portrait and text. Small bubbles (4–8 px radius) rise quickly in six-bubble chains, with uneven spacing, close pairs, occasional overlaps, and wider gaps within each narrow lane. Each lane has a different launch pattern, and small speed differences make the spacing evolve; loops take approximately 4.3–5.6 seconds. Independent gentle sideways oscillation adds natural movement. Large bubbles (20–44 px radius) drift independently over 22–30 seconds. Desktop has three small-bubble lanes and eight large bubbles (26 total); mobile has two lanes and four large bubbles (16 total). The lanes stay outside the main text area. Brighter highlights and outlines make them visible in the free space. A stationary gradient mask reduces bubble opacity to 18% through the reading area, with full visibility near the edges; a rounded clip keeps them inside the blue card. The README picture element selects `hero-still[-mobile]-{theme}.svg` when `prefers-reduced-motion: reduce` is set. This also covers browsers that do not pass that preference into SVG images. The SVG itself has a reduced-motion rule for standalone viewing. Bubble positions, sizes, speed, and opacity are editable in `floating_bubbles()` in the generator.

The avatar is this account's public GitHub avatar. Icons are Font Awesome Free 6.x by Fonticons, Inc.; their original [license](../assets/profile/source/icons/LICENSE.txt) is included. University source files and conversion provenance are documented in [school mark sources](../assets/profile/source/schools/SOURCES.md).
