# Profile presentation assets

The README uses native Markdown for content and links, with locally stored PNG cards for the rounded layout that GitHub cannot style directly. Light, dark, desktop, and mobile variants share the editable source in [profile-cards.html](profile-cards.html).

Serve the repository over HTTP and open `docs/profile-cards.html?asset=hero`. Capture the exact card bounds as PNG. Add `&theme=dark` for dark mode or `&mobile=1` for the mobile hero and education cards.

| Asset | Desktop bounds | Mobile bounds |
| --- | --- | --- |
| hero | 1200 × 320 | 390 × 422 |
| education | 1200 × 326 | 390 × 440 |
| website / scholar | 240 × 80 | same |
| cv | 160 × 80 | same |
| linkedin | 260 × 80 | same |
| email | 210 × 80 | same |

Save as `assets/profile/{asset}[-mobile]-{light|dark}.png`. Buttons display at half their capture size. Responsive picture sources select the appropriate hero and education image; alternative text and an expandable education transcript preserve readable content.

The avatar is this account's public GitHub avatar. Icons are Font Awesome Free 6.x by Fonticons, Inc., recolored blue; their original [license](../assets/profile/source/icons/LICENSE.txt) is included. No reference-profile biography, photograph, university logos, or achievements were copied.
