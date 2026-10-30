"""Editable bilingual SVG figures for introduction slides; no external artwork."""
from pathlib import Path
from html import escape
from math import hypot
ROOT=Path(__file__).parent
BLUE='#1585b4'; DARK='#18344b'; GRAY='#546573'; ACCENT='#3886ad'
class Figure:
 def __init__(self,h=400):
  self.h=h; self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="{h}" viewBox="0 0 1040 {h}"><defs><marker id="arrow" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="14" refY="9" orient="auto"><path d="M2,2 L18,9 L2,16 Z" fill="{ACCENT}"/></marker></defs><rect width="1040" height="{h}" fill="white"/>']
 def text(self,x,y,lines,size=25,color=DARK,weight=400,anchor='middle'):
  if isinstance(lines,str):lines=[lines]
  for i,line in enumerate(lines):self.parts.append(f'<text x="{x}" y="{y+i*(size+8)}" text-anchor="{anchor}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(line)}</text>')
 # Card style shared with the Web Applications decks: soft shadow, light border, left accent bar.
 # The first line is a bold title; further lines are a smaller grey description.
 def box(self,x,y,w,h,lines,size=25):
  if isinstance(lines,str):lines=[lines]
  inset=min(28,h*.28)
  self.parts.append(f'<rect x="{x+1}" y="{y+5}" width="{w-2}" height="{h}" rx="16" fill="#24445c" opacity=".035"/>'
   f'<rect x="{x}" y="{y+2}" width="{w}" height="{h}" rx="16" fill="#24445c" opacity=".025"/>'
   f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#f8fbfd" stroke="#c6dbe8" stroke-width="1.2"/>'
   f'<rect x="{x+12}" y="{y+inset}" width="7" height="{h-2*inset}" rx="3.5" fill="{ACCENT}"/>')
  sub=max(18,round(size*.78)); rest=lines[1:]
  group=size*1.15+(10+len(rest)*(sub+6)-6 if rest else 0); top=y+(h-group)/2
  cx=x+w/2+(6 if w>200 else 9)
  self.text(cx,top+size*.82,lines[0],size,DARK,600)
  for i,line in enumerate(rest):self.text(cx,top+size*1.15+10+sub*.82+i*(sub+6),line,sub,GRAY)
 def arrow(self,points,label=None,lx=0,ly=0):
  path = f'M {points[0][0]} {points[0][1]}'
  for i in range(1, len(points)-1):
   previous, corner, following = points[i-1], points[i], points[i+1]
   incoming = hypot(corner[0]-previous[0], corner[1]-previous[1])
   outgoing = hypot(following[0]-corner[0], following[1]-corner[1])
   if not incoming or not outgoing:
    continue
   radius = min(9, incoming/2, outgoing/2)
   before = [corner[j] + (previous[j]-corner[j])*radius/incoming for j in (0,1)]
   after = [corner[j] + (following[j]-corner[j])*radius/outgoing for j in (0,1)]
   path += f' L {before[0]} {before[1]} Q {corner[0]} {corner[1]} {after[0]} {after[1]}'
  path += f' L {points[-1][0]} {points[-1][1]}'
  self.parts.append(f'<path d="{path}" fill="none" stroke="{ACCENT}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arrow)"/>')
  if label:self.text(lx,ly,label,20,GRAY)
 def line(self,x1,y1,x2,y2):self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BLUE}" stroke-width="3"/>')
 def save(self,name,lang): (ROOT/f'{name}.{lang}.svg').write_text(''.join(self.parts)+'</svg>')
for lang in ['hr','en']:
 def tr(hr,en):return hr if lang=='hr' else en
 # Attendance: process and discussion, without inventing form fields or attendance rules.
 f=Figure(340)
 steps=[tr(['Otvorite poveznicu','ili skenirajte QR'],['Open the link','or scan the QR']),tr(['Evidentirajte','prisutnost'],['Record','your presence']),tr(['Sudjelujte','u raspravi'],['Join','the discussion'])]
 for i,lines in enumerate(steps):
  x=35+i*345;f.text(x+135,52,str(i+1),30,BLUE,700);f.box(x,82,270,110,lines)
  if i<2:f.arrow([(x+270,137),(x+330,137)])
 f.text(520,258,tr('Pitajte · usporedite alternative · objasnite odluke','Ask questions · compare alternatives · explain decisions'),25)
 f.text(520,310,tr('Strelice prikazuju redoslijed koraka.','Arrows show the order of steps.'),18,GRAY);f.save('attendance-explained',lang)
 # Practical work: two typical project types side by side.
 f=Figure(340)
 for x0,title,sub,legend in [(0,tr('Mikroservisi','Microservices'),tr('usluge komuniciraju zahtjevima i porukama','services communicate via requests and messages'),tr('Strelice: zahtjevi; odgovori su izostavljeni.','Arrows: requests; replies are omitted.')),
  (535,tr('Obrada podataka','Data processing'),tr('podijeli, obradi paralelno, objedini','split, process in parallel, combine'),tr('Strelice: tok podataka.','Arrows: data flow.'))]:
  f.parts.append(f'<rect x="{x0+1}" y="1" width="503" height="336" rx="18" fill="#f3f8fb" stroke="#d4e3ec"/>')
  f.text(x0+26,48,title,28,DARK,700,'start');f.text(x0+26,82,sub,19,GRAY,400,'start');f.text(x0+252,310,legend,17,GRAY)
 f.box(20,155,115,70,tr('Klijent','Client'),19);f.box(185,155,125,70,tr('Usluga A','Service A'),19);f.box(360,118,125,56,tr('Usluga B','Service B'),19);f.box(360,206,125,56,tr('Usluga C','Service C'),19)
 f.arrow([(139,190),(181,190)])
 for y in [146,234]:f.arrow([(310,190),(332,190),(332,y),(356,y)])
 f.box(555,155,115,70,tr('Podaci','Data'),19);f.box(715,118,125,56,tr('Proces 1','Process 1'),19);f.box(715,206,125,56,tr('Proces 2','Process 2'),19);f.box(885,155,130,70,tr('Rezultat','Result'),19)
 for y in [146,234]:f.arrow([(670,190),(692,190),(692,y),(711,y)]);f.arrow([(840,y),(862,y),(862,190),(881,190)])
 f.save('practical-work',lang)
 # AI ownership loop.
 f=Figure(290)
 boxes=[tr(['VI određujete','zahtjeve i arhitekturu'],['YOU set requirements','and choose architecture']),tr(['AI predlaže','kod'],['AI proposes','code']),tr(['VI provjeravate','testirate i obrazlažete'],['YOU review','test and justify choices'])]
 for i,lines in enumerate(boxes):
  x=15+i*350;f.box(x,35,310,120,lines,size=23)
  if i<2:f.arrow([(x+310,95),(x+340,95)])
 f.arrow([(870,155),(870,225),(170,225),(170,160)]);f.text(520,212,tr('Vi vodite sljedeću doradu','You guide the next revision'),22,GRAY)
 f.text(520,280,tr('Strelice prikazuju tijek rada i doradu.','Arrows show the workflow and revision loop.'),18,GRAY);f.save('ai-responsibility',lang)
 # Course passing: two parallel inputs and alternative completion paths.
 f=Figure(450)
 f.box(15,30,230,80,tr(['Prijavite projekt','i radite na njemu'],['Register a project','and work on it']),size=22)
 f.box(15,145,230,80,tr(['Skupljajte bodove','na vježbama'],['Collect points','in practical classes']),size=22)
 f.arrow([(245,70),(275,70),(275,128),(310,128)]);f.arrow([(245,185),(275,185),(275,128)])
 f.box(315,85,240,85,tr(['Predajte','projekt'],['Submit','the project']))
 f.arrow([(555,128),(605,128)])
 f.box(610,65,405,125,tr(['Nastavnik odlučuje o oslobođenju','Prijavite ispitni rok na oba puta'],['Lecturer decides exemption','Register for an exam date either way']),size=22)
 f.arrow([(815,190),(815,245),(675,245),(675,278)],tr('Nema oslobođenja','Not exempt'),805,230)
 f.arrow([(1015,130),(1030,130),(1030,330),(1010,330)],tr('Oslobođeni','Exempt'),953,263)
 f.box(525,283,290,94,tr(['Rezervirajte obranu','Obrana i usmeni ispit'],['Book the defence','Defence + oral exam']),size=22)
 f.box(865,290,145,80,tr(['Ocjena','u ISVU'],['Grade','in ISVU']),size=22)
 f.arrow([(815,330),(860,330)]);f.text(839,305,tr('Prolaz','Pass'),17,GRAY)
 f.arrow([(575,377),(575,418),(370,418),(370,210),(650,210),(650,195)],None)
 f.text(250,348,tr(['Neuspjeh: ponovno','prijavite ispitni rok'],['Unsuccessful: register','for another exam date']),21,GRAY)
 f.text(520,436,tr('Strelice prikazuju slijed; dvije početne grane teku paralelno.','Arrows show sequence; the first two branches run in parallel.'),18,GRAY)
 f.save('course-completion',lang)
 # Deadlines use constraints, no invented calendar dates or equal spacing; booking lives in the slide text.
 f=Figure(170)
 for x,label in [(15,tr('Predaja','Submission')),(425,tr('Obrana','Defence')),(835,tr('Ispitni rok','Exam date'))]:f.box(x,30,190,70,label,24)
 f.arrow([(209,65),(419,65)],tr('≥ 3 radna dana','≥ 3 working days'),314,48)
 f.arrow([(619,65),(829,65)],tr('najkasnije do','no later than'),724,48)
 f.text(520,150,tr('Strelice: vremenski uvjeti; razmaci nisu u mjerilu.','Arrows: timing constraints; spacing is not to scale.'),18,GRAY);f.save('deadlines',lang)
 # Oral-exam steps, adapted from the Web Applications orientation deck for distributed projects.
 def steps(name,items,legend,h=280,y=35,ly=200):
  f=Figure(h)
  for i,(title,detail) in enumerate(items):
   x=15+i*350
   f.box(x,y,290,130,[title,detail],27)
   if i<len(items)-1:f.arrow([(x+300,y+65),(x+346,y+65)])
  f.text(520,y+ly,legend,20,GRAY);f.save(name,lang)
 steps('project-evidence',[tr(('Predvidi','očekivano ponašanje'),('Predict','expected behaviour')),tr(('Pokaži','kod, poruke i logove'),('Show','code, messages, logs')),tr(('Objasni','rezultat i uzrok ispada'),('Explain','result and failure cause'))],tr('Slijeva nadesno: koraci demonstracije jedne funkcionalnosti na usmenom.','Left to right: demonstrating one feature at the oral exam.'))
 # Explaining a change on one's own code replaces a live code change (lecturer, 2026-10-13).
 steps('design-change',[tr(('Gdje?','usluge, datoteke, poruke'),('Where?','services, files, messages')),tr(('Kako?','koraci izmjene'),('How?','steps of the change')),tr(('Posljedice?','ispadi, stanje, testiranje'),('Consequences?','failures, state, testing'))],tr('Slijeva nadesno: objašnjenje dorade na vlastitom kodu, uz potpitanja nastavnika.','Left to right: explaining a change on your own code, with follow-up questions.'),210,12,180)
