"""Генератор уникальных SVG-иконок для продуктов."""

SVG_TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.42"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.12"/>
    </linearGradient>
    <filter id="s" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="2" stdDeviation="1.8" flood-color="#000000" flood-opacity="0.25"/>
    </filter>
  </defs>
  <rect x="2" y="2" width="60" height="60" rx="15" fill="{bg}"/>
  <rect x="2" y="2" width="60" height="60" rx="15" fill="url(#g)"/>
  {content}
  <rect x="2.5" y="2.5" width="59" height="59" rx="14.5" fill="none" stroke="#ffffff" stroke-opacity="0.45"/>
</svg>'''


def _svg(bg, content):
    return SVG_TEMPLATE.format(bg=bg, content=content)


# slug -> SVG inner content (distinctive mini-illustrations)
ICON_SHAPES = {
    'kuritsa': _svg('#FFE0B2', '<ellipse cx="32" cy="38" rx="16" ry="12" fill="#E65100"/><path d="M20 30 Q32 18 44 30" stroke="#BF360C" stroke-width="3" fill="none"/><circle cx="28" cy="32" r="2" fill="#3E2723"/>'),
    'govyadina': _svg('#FFCCBC', '<rect x="14" y="24" width="36" height="22" rx="6" fill="#BF360C"/><path d="M18 28 h28 M18 34 h28 M18 40 h28" stroke="#FFAB91" stroke-width="2"/>'),
    'svinina': _svg('#FFCCBC', '<ellipse cx="32" cy="34" rx="18" ry="14" fill="#D84315"/><ellipse cx="32" cy="34" rx="10" ry="8" fill="#FFAB91" opacity="0.6"/>'),
    'indeika': _svg('#FFF3E0', '<ellipse cx="32" cy="36" rx="14" ry="16" fill="#F57C00"/><circle cx="32" cy="22" r="8" fill="#FFB74D"/><circle cx="30" cy="21" r="1.5" fill="#3E2723"/>'),
    'vetchina': _svg('#FFEBEE', '<rect x="16" y="22" width="32" height="20" rx="4" fill="#E57373"/><rect x="20" y="26" width="8" height="12" rx="2" fill="#FFCDD2"/><rect x="36" y="26" width="8" height="12" rx="2" fill="#FFCDD2"/>'),
    'kolbasa': _svg('#FCE4EC', '<rect x="12" y="28" width="40" height="14" rx="7" fill="#C62828"/><circle cx="22" cy="35" r="3" fill="#FFCDD2" opacity="0.5"/><circle cx="32" cy="35" r="3" fill="#FFCDD2" opacity="0.5"/><circle cx="42" cy="35" r="3" fill="#FFCDD2" opacity="0.5"/>'),

    'losos': _svg('#E3F2FD', '<ellipse cx="32" cy="34" rx="20" ry="10" fill="#FF8A65"/><path d="M12 34 L20 28 L20 40 Z" fill="#FF7043"/><circle cx="42" cy="32" r="2" fill="#1A237E"/>'),
    'tunets': _svg('#E0F7FA', '<ellipse cx="32" cy="34" rx="18" ry="11" fill="#455A64"/><path d="M14 34 L22 29 L22 39 Z" fill="#263238"/><circle cx="40" cy="32" r="2" fill="#fff"/>'),
    'krevetki': _svg('#FFF8E1', '<path d="M20 40 Q24 24 28 40 Q32 24 36 40 Q40 24 44 40" stroke="#FF6F00" stroke-width="4" fill="none" stroke-linecap="round"/>'),
    'kalmary': _svg('#F3E5F5', '<ellipse cx="32" cy="36" rx="12" ry="14" fill="#E1BEE7"/><path d="M24 44 Q20 52 18 56 M28 46 Q26 54 24 58 M36 46 Q38 54 40 58 M40 44 Q44 52 46 56" stroke="#9C27B0" stroke-width="2" fill="none"/>'),
    'seld': _svg('#E8EAF6', '<ellipse cx="32" cy="34" rx="18" ry="9" fill="#5C6BC0"/><path d="M14 34 L22 30 L22 38 Z" fill="#3949AB"/><path d="M26 30 Q32 26 38 30" stroke="#C5CAE9" stroke-width="2" fill="none"/>'),

    'pomidory': _svg('#FFEBEE', '<circle cx="32" cy="36" r="14" fill="#E53935"/><ellipse cx="32" cy="22" rx="6" ry="4" fill="#43A047"/><path d="M28 20 L32 16 L36 20" stroke="#2E7D32" stroke-width="2" fill="none"/>'),
    'ogurtsy': _svg('#E8F5E9', '<ellipse cx="32" cy="34" rx="10" ry="18" fill="#43A047"/><ellipse cx="28" cy="30" rx="2" ry="4" fill="#A5D6A7" opacity="0.7"/><ellipse cx="36" cy="38" rx="2" ry="4" fill="#A5D6A7" opacity="0.7"/>'),
    'luk': _svg('#FFFDE7', '<circle cx="32" cy="36" r="14" fill="#F9A825"/><path d="M32 22 Q28 30 32 36 Q36 30 32 22" fill="#FDD835"/><path d="M28 20 Q32 14 36 20" stroke="#8D6E63" stroke-width="2" fill="none"/>'),
    'chesnok': _svg('#FFF8E1', '<ellipse cx="28" cy="36" rx="8" ry="12" fill="#FFF9C4" stroke="#F9A825" stroke-width="1"/><ellipse cx="36" cy="36" rx="8" ry="12" fill="#FFF9C4" stroke="#F9A825" stroke-width="1"/><path d="M32 24 Q32 18 32 14" stroke="#8D6E63" stroke-width="2"/>'),
    'morkov': _svg('#FFF3E0', '<path d="M32 14 L36 48 L28 48 Z" fill="#FF9800"/><path d="M30 18 L34 18 M29 24 L35 24 M28 30 L36 30" stroke="#FFE0B2" stroke-width="1.5"/>'),
    'kartofel': _svg('#EFEBE9', '<ellipse cx="32" cy="36" rx="14" ry="16" fill="#8D6E63"/><ellipse cx="28" cy="32" rx="2" ry="3" fill="#A1887F"/><ellipse cx="36" cy="38" rx="2" ry="3" fill="#A1887F"/>'),
    'kapusta': _svg('#E8F5E9', '<circle cx="32" cy="36" r="16" fill="#66BB6A"/><path d="M20 36 Q32 20 44 36 Q32 28 20 36" fill="#43A047"/><path d="M24 40 Q32 30 40 40" stroke="#2E7D32" stroke-width="1.5" fill="none"/>'),
    'perets-sladkiy': _svg('#FFEBEE', '<path d="M32 16 L42 40 Q32 46 22 40 Z" fill="#E53935"/><path d="M30 16 Q32 10 34 16" stroke="#43A047" stroke-width="3" fill="none"/>'),
    'baklazhan': _svg('#F3E5F5', '<ellipse cx="32" cy="36" rx="12" ry="18" fill="#6A1B9A"/><ellipse cx="32" cy="20" rx="4" ry="3" fill="#43A047"/>'),
    'tsukkini': _svg('#E8F5E9', '<ellipse cx="32" cy="36" rx="11" ry="18" fill="#43A047"/><ellipse cx="32" cy="20" rx="3" ry="2" fill="#2E7D32"/>'),
    'svyokla': _svg('#FCE4EC', '<circle cx="32" cy="38" r="14" fill="#AD1457"/><path d="M28 24 L32 16 L36 24" stroke="#43A047" stroke-width="2" fill="none"/>'),
    'griby': _svg('#EFEBE9', '<ellipse cx="32" cy="28" rx="16" ry="10" fill="#8D6E63"/><rect x="26" y="28" width="12" height="16" rx="4" fill="#D7CCC8"/>'),

    'yabloki': _svg('#FFEBEE', '<circle cx="32" cy="36" r="14" fill="#E53935"/><path d="M32 22 L32 16" stroke="#5D4037" stroke-width="2"/><ellipse cx="34" cy="18" rx="4" ry="2" fill="#43A047" transform="rotate(30 34 18)"/>'),
    'banany': _svg('#FFFDE7', '<path d="M18 44 Q28 16 46 28 Q38 40 18 44" fill="#FDD835" stroke="#F9A825" stroke-width="1"/>'),
    'apelsiny': _svg('#FFF3E0', '<circle cx="32" cy="36" r="14" fill="#FF9800"/><circle cx="32" cy="36" r="10" fill="none" stroke="#FFB74D" stroke-width="1"/><path d="M32 22 L32 18" stroke="#43A047" stroke-width="2"/>'),
    'klubnika': _svg('#FFEBEE', '<path d="M32 20 L22 38 Q32 48 42 38 Z" fill="#E53935"/><circle cx="26" cy="32" r="1.5" fill="#FFCDD2"/><circle cx="32" cy="36" r="1.5" fill="#FFCDD2"/><circle cx="38" cy="32" r="1.5" fill="#FFCDD2"/>'),
    'limony': _svg('#FFFDE7', '<ellipse cx="32" cy="36" rx="14" ry="16" fill="#FDD835"/><ellipse cx="32" cy="36" rx="8" ry="10" fill="#FFF59D" opacity="0.5"/>'),
    'vishnya': _svg('#FCE4EC', '<circle cx="26" cy="36" r="8" fill="#C62828"/><circle cx="38" cy="36" r="8" fill="#C62828"/><path d="M32 28 L32 20" stroke="#5D4037" stroke-width="2"/>'),

    'moloko': _svg('#E3F2FD', '<rect x="22" y="16" width="20" height="32" rx="3" fill="#fff" stroke="#90CAF9" stroke-width="2"/><path d="M24 16 Q32 22 40 16" fill="#BBDEFB"/><rect x="26" y="28" width="12" height="14" rx="1" fill="#E3F2FD"/>'),
    'syr': _svg('#FFF8E1', '<path d="M16 40 L32 20 L48 40 Z" fill="#FFC107"/><circle cx="24" cy="36" r="3" fill="#FFE082"/><circle cx="36" cy="34" r="2.5" fill="#FFE082"/>'),
    'slivochnoe-maslo': _svg('#FFFDE7', '<rect x="18" y="24" width="28" height="20" rx="4" fill="#FFF59D" stroke="#F9A825" stroke-width="2"/><path d="M22 28 h20 M22 32 h20 M22 36 h20" stroke="#FFE082" stroke-width="1"/>'),
    'smetana': _svg('#F3E5F5', '<ellipse cx="32" cy="40" rx="16" ry="8" fill="#fff" stroke="#CE93D8" stroke-width="2"/><path d="M20 36 Q32 28 44 36" fill="#F3E5F5"/>'),
    'yogurt': _svg('#E8F5E9', '<path d="M22 20 L26 48 L38 48 L42 20 Z" fill="#fff" stroke="#A5D6A7" stroke-width="2"/><rect x="24" y="30" width="16" height="12" rx="2" fill="#C8E6C9"/>'),
    'slivki': _svg('#FCE4EC', '<rect x="20" y="18" width="24" height="30" rx="4" fill="#fff" stroke="#F48FB1" stroke-width="2"/><ellipse cx="32" cy="34" rx="8" ry="10" fill="#F8BBD0"/>'),
    'tvorog': _svg('#FFFDE7', '<rect x="18" y="26" width="28" height="20" rx="6" fill="#FFF9C4" stroke="#F9A825" stroke-width="2"/><circle cx="26" cy="36" r="2" fill="#FFE082"/><circle cx="32" cy="34" r="2" fill="#FFE082"/><circle cx="38" cy="36" r="2" fill="#FFE082"/>'),

    'yaytsa': _svg('#FFF8E1', '<ellipse cx="32" cy="36" rx="12" ry="16" fill="#FFF9C4" stroke="#F9A825" stroke-width="2"/><ellipse cx="32" cy="36" rx="6" ry="8" fill="#FFEB3B" opacity="0.6"/>'),
    'muka': _svg('#EFEBE9', '<path d="M20 44 L32 18 L44 44 Z" fill="#D7CCC8" stroke="#A1887F" stroke-width="2"/><ellipse cx="32" cy="38" rx="8" ry="4" fill="#fff" opacity="0.6"/>'),
    'sahar': _svg('#E3F2FD', '<rect x="20" y="20" width="24" height="24" rx="4" fill="#fff" stroke="#90CAF9" stroke-width="2"/><path d="M26 28 h12 M26 32 h12 M26 36 h12" stroke="#BBDEFB" stroke-width="2"/>'),
    'med': _svg('#FFF8E1', '<path d="M24 20 L28 44 L36 44 L40 20 Z" fill="#FFC107" stroke="#FF8F00" stroke-width="2"/><rect x="26" y="16" width="12" height="6" rx="2" fill="#FFD54F"/>'),
    'razryhlitel': _svg('#ECEFF1', '<rect x="22" y="18" width="20" height="28" rx="3" fill="#CFD8DC"/><circle cx="32" cy="32" r="6" fill="#fff"/>'),
    'vanil': _svg('#EFEBE9', '<rect x="28" y="16" width="8" height="32" rx="2" fill="#5D4037"/><ellipse cx="32" cy="14" rx="4" ry="2" fill="#8D6E63"/>'),
    'makarony': _svg('#FFF3E0', '<path d="M18 28 Q24 20 30 28 Q36 36 42 28" stroke="#FF9800" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M18 36 Q24 28 30 36 Q36 44 42 36" stroke="#FFB74D" stroke-width="5" fill="none" stroke-linecap="round"/>'),
    'lapsha': _svg('#FFF8E1', '<path d="M16 32 Q32 24 48 32" stroke="#F9A825" stroke-width="3" fill="none"/><path d="M16 38 Q32 30 48 38" stroke="#F9A825" stroke-width="3" fill="none"/><path d="M16 44 Q32 36 48 44" stroke="#F9A825" stroke-width="3" fill="none"/>'),

    'olivkovoe-maslo': _svg('#E8F5E9', '<rect x="24" y="14" width="16" height="34" rx="4" fill="#66BB6A"/><rect x="26" y="18" width="12" height="20" rx="2" fill="#C8E6C9"/><ellipse cx="32" cy="42" rx="6" ry="3" fill="#43A047"/>'),
    'podsolnechnoe-maslo': _svg('#FFFDE7', '<rect x="24" y="14" width="16" height="34" rx="4" fill="#FDD835"/><circle cx="32" cy="28" r="6" fill="#5D4037"/><circle cx="32" cy="28" r="3" fill="#8D6E63"/>'),
    'kokosovoe-maslo': _svg('#EFEBE9', '<circle cx="32" cy="36" r="16" fill="#8D6E63"/><ellipse cx="32" cy="36" rx="10" ry="12" fill="#FFF9C4"/><circle cx="28" cy="32" r="2" fill="#5D4037"/><circle cx="36" cy="34" r="2" fill="#5D4037"/>'),

    'sol': _svg('#ECEFF1', '<rect x="20" y="22" width="24" height="24" rx="4" fill="#fff" stroke="#90A4AE" stroke-width="2"/><circle cx="26" cy="30" r="2" fill="#CFD8DC"/><circle cx="34" cy="28" r="2" fill="#CFD8DC"/><circle cx="30" cy="36" r="2" fill="#CFD8DC"/>'),
    'perec': _svg('#FFEBEE', '<circle cx="32" cy="36" r="14" fill="#37474F"/><circle cx="32" cy="36" r="8" fill="#263238"/><circle cx="30" cy="34" r="2" fill="#455A64"/>'),
    'kurkuma': _svg('#FFF8E1', '<ellipse cx="32" cy="38" rx="12" ry="8" fill="#FF8F00"/><path d="M28 30 Q32 22 36 30" stroke="#F57C00" stroke-width="3" fill="none"/>'),
    'paprika': _svg('#FFEBEE', '<path d="M28 20 L36 20 L38 44 L26 44 Z" fill="#E53935"/><ellipse cx="32" cy="18" rx="4" ry="3" fill="#43A047"/>'),
    'koriandr': _svg('#E8F5E9', '<circle cx="32" cy="36" r="12" fill="#81C784"/><path d="M26 30 L32 22 L38 30 L35 38 L29 38 Z" fill="#43A047"/>'),
    'lavrovyy-list': _svg('#E8F5E9', '<ellipse cx="32" cy="36" rx="8" ry="14" fill="#43A047" transform="rotate(-20 32 36)"/><path d="M28 28 Q32 36 28 44" stroke="#2E7D32" stroke-width="1" fill="none"/>'),
    'zelen': _svg('#E8F5E9', '<path d="M32 16 Q20 28 24 44 M32 16 Q44 28 40 44 M32 16 L32 44" stroke="#43A047" stroke-width="3" fill="none" stroke-linecap="round"/>'),

    'ris': _svg('#FFFDE7', '<ellipse cx="32" cy="38" rx="16" ry="10" fill="#FFF9C4"/><circle cx="24" cy="36" r="2" fill="#F9A825"/><circle cx="32" cy="34" r="2" fill="#F9A825"/><circle cx="40" cy="36" r="2" fill="#F9A825"/><circle cx="28" cy="40" r="2" fill="#F9A825"/><circle cx="36" cy="40" r="2" fill="#F9A825"/>'),
    'grechka': _svg('#EFEBE9', '<ellipse cx="32" cy="38" rx="16" ry="10" fill="#5D4037"/><circle cx="24" cy="36" r="2.5" fill="#8D6E63"/><circle cx="32" cy="34" r="2.5" fill="#8D6E63"/><circle cx="40" cy="36" r="2.5" fill="#8D6E63"/>'),
    'ovsyanka': _svg('#FFF3E0', '<ellipse cx="32" cy="38" rx="16" ry="10" fill="#D7CCC8"/><circle cx="26" cy="36" r="3" fill="#A1887F"/><circle cx="34" cy="34" r="3" fill="#A1887F"/><circle cx="38" cy="38" r="3" fill="#A1887F"/>'),
    'chechevitsa': _svg('#FFEBEE', '<ellipse cx="32" cy="38" rx="16" ry="10" fill="#FF7043"/><circle cx="26" cy="36" r="2" fill="#BF360C"/><circle cx="34" cy="34" r="2" fill="#BF360C"/><circle cx="38" cy="38" r="2" fill="#BF360C"/>'),
    'fasol': _svg('#EFEBE9', '<ellipse cx="26" cy="36" rx="6" ry="10" fill="#8D6E63" transform="rotate(-30 26 36)"/><ellipse cx="38" cy="36" rx="6" ry="10" fill="#A1887F" transform="rotate(30 38 36)"/>'),
    'goroh': _svg('#E8F5E9', '<circle cx="26" cy="36" r="6" fill="#66BB6A"/><circle cx="38" cy="36" r="6" fill="#81C784"/><circle cx="32" cy="28" r="6" fill="#43A047"/>'),

    'mindal': _svg('#EFEBE9', '<ellipse cx="32" cy="36" rx="10" ry="14" fill="#D7CCC8" stroke="#A1887F" stroke-width="2"/><ellipse cx="32" cy="36" rx="5" ry="8" fill="#BCAAA4"/>'),
    'gretskie-orehi': _svg('#EFEBE9', '<circle cx="32" cy="36" r="14" fill="#8D6E63"/><path d="M24 36 Q32 24 40 36 Q32 48 24 36" fill="#5D4037"/>'),
    'funduk': _svg('#FFF3E0', '<circle cx="32" cy="36" r="12" fill="#8D6E63"/><ellipse cx="32" cy="36" rx="6" ry="10" fill="#A1887F"/>'),
    'izyum': _svg('#EFEBE9', '<ellipse cx="28" cy="36" rx="5" ry="7" fill="#5D4037"/><ellipse cx="36" cy="34" rx="5" ry="7" fill="#6D4C41"/><ellipse cx="32" cy="42" rx="5" ry="7" fill="#4E342E"/>'),
    'kuraga': _svg('#FFF3E0', '<circle cx="28" cy="36" r="7" fill="#FF9800"/><circle cx="38" cy="36" r="7" fill="#FFB74D"/><circle cx="33" cy="28" r="6" fill="#F57C00"/>'),

    'tomatnaya-pasta': _svg('#FFEBEE', '<rect x="22" y="18" width="20" height="28" rx="3" fill="#E53935"/><rect x="24" y="14" width="16" height="6" rx="2" fill="#C62828"/>'),
    'mayonez': _svg('#FFFDE7', '<rect x="24" y="16" width="16" height="32" rx="3" fill="#fff" stroke="#F9A825" stroke-width="2"/><ellipse cx="32" cy="32" rx="5" ry="8" fill="#FFF9C4"/>'),
    'hleb': _svg('#FFF3E0', '<rect x="16" y="28" width="32" height="18" rx="8" fill="#D7A86E"/><path d="M20 32 Q32 24 44 32" stroke="#A1887F" stroke-width="2" fill="none"/>'),
    'ukrop': _svg('#E8F5E9', '<path d="M32 14 Q24 24 22 44 M32 14 Q40 24 42 44" stroke="#43A047" stroke-width="2.5" fill="none"/><path d="M28 28 L36 28 M26 34 L38 34" stroke="#66BB6A" stroke-width="1.5"/>'),
}


def get_icon_svg(slug):
    return ICON_SHAPES.get(slug, _svg('#E8F5E9', '<circle cx="32" cy="36" r="12" fill="#66BB6A"/><text x="32" y="40" text-anchor="middle" font-size="14" fill="#fff">?</text>'))
