"""Original bilingual client-observation timeline for the 101 ms exercise."""
from html import escape
from pathlib import Path
import subprocess

ROOT = Path(__file__).parent
for lang in ('hr', 'en'):
    def t(hr, en):
        return escape(hr if lang == 'hr' else en)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="300" viewBox="0 0 1120 300">
<rect width="1120" height="300" fill="white"/>
<g font-family="Arial, sans-serif" fill="#18344b">
<text x="70" y="35" font-size="24">{t('Što klijent vidi', 'What the client observes')}</text>
<path d="M100 112 V92 H800 V112" fill="none" stroke="#607582" stroke-width="2"/>
<text x="450" y="77" text-anchor="middle" font-size="24">{t('Odgovor obično stigne unutar 100 ms', 'Reply usually arrives within 100 ms')}</text>
<path d="M100 162 H980" fill="none" stroke="#1585b4" stroke-width="5"/>
<path d="M970 155 L985 162 L970 169" fill="#1585b4"/>
<circle cx="100" cy="162" r="7" fill="#1585b4"/>
<path d="M800 132 V185" stroke="#607582" stroke-width="2" stroke-dasharray="5 5"/>
<circle cx="980" cy="162" r="10" fill="white" stroke="#b33e44" stroke-width="3"/>
<text x="100" y="211" text-anchor="middle" font-size="24">0 ms</text>
<text x="800" y="211" text-anchor="middle" font-size="24">100 ms</text>
<text x="980" y="211" text-anchor="middle" font-size="24" fill="#b33e44">101 ms</text>
<text x="70" y="247" font-size="23">{t('Zahtjev poslan', 'Request sent')}</text>
<text x="1040" y="247" text-anchor="end" font-size="23" fill="#b33e44">{t('Još nema odgovora', 'Still no reply')}</text>
<text x="480" y="151" text-anchor="middle" font-size="23" fill="#1585b4">{t('Čekanje na odgovor', 'Waiting for a reply')}</text>
<text x="560" y="290" text-anchor="middle" font-size="18" fill="#607582">{t('Vrijeme teče udesno. Razmaci nisu u mjerilu.', 'Time moves right. Spacing is not to scale.')}</text>
</g></svg>'''
    path = ROOT / f'reply-wait.{lang}.svg'
    # SVGs are now editable masters; retain the reviewed artwork when exporting.
    subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-f', 'pdf', '-o',
                    str(path.with_suffix('.pdf')), str(path)], check=True)
