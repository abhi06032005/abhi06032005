with open('README.md', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Match from <div align="center"> to the first </div> after the hero section
old = """<div align="center">

<!-- ═══════════════════════════════════════════════════════════════════ -->
<!--  🏴‍☠️ HERO SECTION: REAL ONE PIECE CHARACTERS (LUFFY & ZORO ON SUNNY) -->
<!-- ═══════════════════════════════════════════════════════════════════ -->
<a href="https://github.com/abhi06032005">
  <img src="./assets/onepiece-banner.svg" width="100%" alt="Abhijeet Nayak \u2014 Luffy Gear 5 & Zoro One Piece Banner" />
</a>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════ -->
<!--  ⚡ DYNAMIC PIRATE KING TYPING HEADLINE                             -->
<!-- ═══════════════════════════════════════════════════════════════════ -->"""

new = """<div align="center">

<!-- ══════════════════════════════════════════════════════════════════ -->
<!--  🎨 Dot-Matrix Portrait                                           -->
<!-- ══════════════════════════════════════════════════════════════════ -->
<a href="https://github.com/abhi06032005">
  <img src="./assets/dot-portrait.svg" width="260" alt="Abhijeet Nayak Dot-Matrix Portrait" />
</a>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════ -->
<!--  ⚡ DYNAMIC PIRATE KING TYPING HEADLINE                             -->
<!-- ═══════════════════════════════════════════════════════════════════ -->"""

if old in content:
    new_content = content.replace(old, new, 1)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Replacement successful')
else:
    print('Old not found with broad pattern')
    # Try simplest: just replace the img source
    pass