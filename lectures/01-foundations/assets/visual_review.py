"""Additional lecture figures. Croatian labels first, English translation second.
Run with Python; SVG to vector PDF uses rsvg-convert. No external artwork.
"""
from pathlib import Path
from html import escape
import subprocess
ROOT=Path(__file__).parent
INK='#18344b'; BLUE='#1585b4'; RED='#b33e44'; GREY='#607582'
class Figure:
 def __init__(self,h):
  self.h=h; self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="{h}" viewBox="0 0 1120 {h}"><rect width="1120" height="{h}" fill="white"/><defs><marker id="a" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L10 5L0 10Z" fill="{BLUE}"/></marker></defs>']
 def text(self,x,y,s,size=24,color=INK,anchor='middle'):
  self.parts.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>')
 def box(self,x,y,w,h,s,fill='#edf8fc',stroke=BLUE):
  self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'); self.text(x+w/2,y+h/2+8,s)
 def line(self,x,y,X,Y,arrow=False,dash=False):
  self.parts.append(f'<path d="M{x} {y}L{X} {Y}" fill="none" stroke="{BLUE}" stroke-width="2.4" stroke-linecap="round"'+(' marker-end="url(#a)"' if arrow else '')+(' stroke-dasharray="6 7"' if dash else '')+'/>')
 def save(self,name,lang):
  path=ROOT/f'{name}.{lang}.svg';path.write_text(''.join(self.parts)+'</svg>'); subprocess.run(['/opt/homebrew/bin/rsvg-convert','-f','pdf','-o',str(path.with_suffix('.pdf')),str(path)],check=True)
for lang in ['hr','en']:
 def t(hr,en):return hr if lang=='hr' else en
 d=Figure(290)
 d.box(80,25,960,235,'',fill='#fafcfd',stroke='#bccdd7')
 d.text(115,65,t('Portal za predaju projekata','Project-submission portal'),24,anchor='start')
 d.line(80,88,1040,88)
 d.text(125,140,'project.zip',32,anchor='start');d.text(995,140,'20 MB',24,anchor='end')
 d.text(125,181,t('Unity projekt: kod, scene, slike i zvukovi','Unity project: code, scenes, images and sounds'),23,anchor='start')
 d.text(560,232,t('Isteklo je vrijeme čekanja na odgovor','Request timed out'),30,RED)
 d.save('upload-timeout',lang)
 d=Figure(265)
 for y,label in [(70,t('A · prvi pokušaj','A · original attempt')),(160,t('B · ponovni pokušaj','B · retry'))]:
  d.text(15,y+8,label,22,anchor='start');d.line(245,y,1090,y,True)
 for x,y,label in [(390,70,t('Nema zapisa','No entry')),(570,160,t('Nema zapisa','No entry')),(770,70,t('Stvori zapis','Create entry')),(950,160,t('Stvori zapis','Create entry'))]:
  d.box(x-85,y-27,170,54,label)
 d.text(560,235,t('Vrijeme teče udesno. Ista predaja, dva prihvaćena zapisa.','Time moves right. Same submission, two accepted entries.'),25,RED)
 # retry-race.hr/en.svg are editable masters; render with just headless-preview.
 d=Figure(190)
 d.text(280,35,t('Kršenje sigurnosti','Safety violation'),25,RED)
 d.text(840,35,t('Kršenje napredovanja','Liveness violation'),25,RED)
 d.box(60,60,195,55,t('Zapis 1','Entry 1'));d.box(300,60,195,55,t('Zapis 2','Entry 2'))
 d.text(280,153,t('Ista namjeravana predaja','Same intended submission'),22)
 d.text(620,90,t('Čekanje','Pending'),24,anchor='start');d.line(750,83,1060,83,True,True)
 d.text(840,132,t('Nikad prihvaćeno','Never accepted'),23)
 d.text(840,169,t('Iako vrijede pretpostavke napretka','Despite the progress assumptions holding'),19)
 d.save('safety-liveness',lang)
 d=Figure(390)
 rows=[('Crash-stop',t('Radi','Running'),t('Staje zauvijek','Stops permanently')),('Crash-recovery',t('Pad','Crash'),t('Ponovno radi','Restarts')),('Byzantine',t('Čvor','Node'),t('Proturječne poruke','Conflicting messages'))]
 for i,(label,a,b) in enumerate(rows):
  y=55+i*115;d.text(15,y+8,label,27,anchor='start');d.box(290,y-28,190,56,a);d.line(480,y,650,y,True);d.box(650,y-28,435,56,b)
 d.text(865,216,t('Navedi koje je stanje trajno','Specify which state is durable'),20,GREY)
 d.text(865,331,t('Jedan primjer proizvoljnog ponašanja','One example of arbitrary behaviour'),20,GREY)
 d.text(560,382,t('Strelice prikazuju tijek ili slanje poruka, ne otkrivanje pada.','Arrows show progression or messages, not crash detection.'),20,GREY)
 d.save('node-models',lang)
 d=Figure(540)
 # Separated bands; all delta brackets retain the same 160-unit width.
 d.parts.append('<rect x="0" y="155" width="1120" height="145" fill="#f2f7fa"/>')
 def message(start,end,y,bound,label):
  d.line(start,y,end,y,True)
  d.line(start,y-8,start,y+8)
  d.text(start,y+30,t('Slanje','Send'),20)
  d.text(end,y+30,t('Primitak','Receive'),20)
  d.line(bound,y-18,bound,y+10,dash=True)
  d.line(start,y-33,bound,y-33)
  d.line(start,y-38,start,y-28);d.line(bound,y-38,bound,y-28)
  d.text((start+bound)/2,y-45,label,22)
 d.text(20,82,t('Sinkroni','Synchronous'),27,anchor='start')
 message(320,425,95,480,'Δ')
 d.text(810,76,t('Kašnjenje ≤ Δ','Delay ≤ Δ'),27)
 d.text(810,110,t('Poznata granica uvijek vrijedi','Known bound always holds'),23)
 d.text(20,224,t('Asinkroni','Asynchronous'),27,anchor='start')
 message(320,620,240,480,t('Odabrani timeout','Chosen timeout'))
 d.text(855,216,t('Moguć kasni primitak','Late arrival is allowed'),24)
 d.text(855,250,t('Nema zajamčene granice','No guaranteed delay bound'),23)
 d.text(20,352,t('Djelomično','Partially'),27,anchor='start')
 d.text(20,385,t('sinkroni','synchronous'),27,anchor='start')
 d.text(430,340,t('Prije stabilizacije','Before stabilization'),24)
 d.text(430,371,t('Kašnjenje može biti > Δ','Delay may exceed Δ'),22)
 d.text(875,340,t('Nakon stabilizacije','After stabilization'),24)
 d.text(875,371,t('Kašnjenje ≤ Δ','Delay ≤ Δ'),22)
 message(300,555,448,460,'Δ')
 message(790,895,448,950,'Δ')
 d.line(660,390,660,487,dash=True)
 d.text(660,520,t('Trenutak stabilizacije: nije poznat unaprijed','Stabilization time: unknown in advance'),24,GREY)
 d.text(1090,25,t('Vrijeme →','Time →'),21,GREY,anchor='end')
 # timing-models.hr/en.svg are maintained as editable SVG masters; do not overwrite.
