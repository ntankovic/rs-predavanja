"""Editable vector diagrams for lecture 01. Run with PyMuPDF installed."""
from pathlib import Path
from html import escape
import pymupdf as fitz
ROOT=Path(__file__).resolve().parent
INK='#18344b'; BLUE='#1585b4'; LIGHT='#e6f6fd'; RED='#b33e44'; ORANGE='#b56a21'

class Diagram:
 def __init__(self,w=1120,h=460):
  self.w=w;self.h=h
  self.items=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="white"/>']
 def text(self,x,y,text,size=24,color=INK,anchor='middle',weight='normal'):
  self.items.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(text)}</text>')
 def line(self,x1,y1,x2,y2,color=INK,width=3,dash=False):
  self.items.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="8 7"' if dash else '')+'/>')
 def arrow(self,x1,y1,x2,y2,color=INK,dash=False):
  import math
  self.line(x1,y1,x2,y2,color,3,dash)
  a=math.atan2(y2-y1,x2-x1);size=12
  pts=[(x2,y2),(x2-size*math.cos(a-.45),y2-size*math.sin(a-.45)),(x2-size*math.cos(a+.45),y2-size*math.sin(a+.45))]
  self.items.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{color}"/>')
 def rect(self,x,y,w,h,fill=LIGHT,stroke=BLUE):
  self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
 def box(self,x,y,w,h,label,sub=None,fill=LIGHT,stroke=BLUE):
  # Reserve 20 drawing units on each side, including for longer labels.
  def fitted(text,size,font):
   width=fitz.get_text_length(text,fontname=font,fontsize=size)
   return min(size,size*(w-40)/max(width,1))
  self.rect(x,y,w,h,fill,stroke)
  # SVG y coordinates are baselines: center the visible text block, not
  # the first baseline. Use glyph bounds so fitted font sizes stay centered.
  lines=[(label,fitted(label,25,'hebo'),'hebo','bold')]
  if sub:lines.append((sub,fitted(sub,20,'helv'),'helv','normal'))
  metrics=[]
  for text,size,font_name,weight in lines:
   font=fitz.Font(font_name)
   bounds=[font.glyph_bbox(ord(char)) for char in text if not char.isspace()]
   ascent=max(b.y1 for b in bounds)*size
   descent=-min(b.y0 for b in bounds)*size
   metrics.append((text,size,weight,ascent,descent))
  gap=9
  total=sum(ascent+descent for _,_,_,ascent,descent in metrics)+gap*(len(metrics)-1)
  top=y+(h-total)/2
  for text,size,weight,ascent,descent in metrics:
   self.text(x+w/2,top+ascent,text,size,weight=weight)
   top+=ascent+descent+gap
 def save(self,name):
  svg=''.join(self.items)+'</svg>';(ROOT/(name+'.svg')).write_text(svg)
  doc=fitz.open(stream=svg.encode(),filetype='svg');pdf=fitz.open('pdf',doc.convert_to_pdf());pdf.save(ROOT/(name+'.pdf'))

# system-map and partial-failure moved to draw_system_map.py (bilingual, card style, 2026-10-13).

d=Diagram(h=460)
d.text(560,35,'Two tasks: A and B',27,weight='bold')
d.text(25,95,'Concurrent, one worker',25,anchor='start',weight='bold')
d.text(95,164,'Worker',21)
for i,label in enumerate(['A1','B1','A2','B2','A3','B3']):
 x=195+i*140;col=LIGHT if label[0]=='A' else '#fff0dc';edge=BLUE if label[0]=='A' else ORANGE
 d.rect(x,125,125,65,col,edge);d.text(x+62,166,label,25)
d.text(25,255,'Parallel, two workers',25,anchor='start',weight='bold')
for row,task in enumerate(['A','B']):
 y=285+row*85;d.text(95,y+39,'Worker '+str(row+1),21)
 for i in range(3):
  x=195+i*140;d.rect(x,y,125,60,LIGHT if task=='A' else '#fff0dc',BLUE if task=='A' else ORANGE);d.text(x+62,y+38,task+str(i+1),25)
d.arrow(710,350,1060,350);d.text(885,390,'Time moves right',21)
# concurrency.svg is now the hand-edited master. Rebuild its PDF with
# just headless-preview lectures/01-foundations/assets/concurrency.svg

d=Diagram(h=430)
d.text(280,40,'Local call',28,weight='bold');d.text(840,40,'Remote request',28,weight='bold')
d.rect(35,85,480,225,'#f7fafb','#9cafba');d.text(275,117,'One process / address space',21)
d.box(65,160,160,80,'Caller');d.box(325,160,160,80,'Function')
d.arrow(225,181,325,181);d.arrow(325,224,225,224);d.text(275,270,'Control and return value',20)
d.box(585,160,180,80,'Client');d.box(905,160,180,80,'Service')
d.arrow(765,176,905,176);d.text(925,140,'request',20)
d.arrow(905,226,765,226);d.text(755,277,'reply',20)
d.line(835,80,835,320,ORANGE,2,True);d.text(835,355,'Network boundary',22,color=ORANGE)
d.text(280,390,'A local call can fail too.',22);d.text(840,390,'Remote outcome may be unknown.',22)
d.save('local-remote')

def timeout(name,success):
 d=Diagram(h=490)
 d.text(560,35,'B · Request applied, reply lost' if success else 'A · Complete request never arrives',27,weight='bold')
 for x,label in [(190,'Student browser'),(730,'Submission service')]:
  d.text(x,95,label,25,weight='bold');d.arrow(x,125,x,435,'#8da1ad')
 d.text(965,125,'Time moves down',20)
 if success:
  d.arrow(190,155,730,205);d.text(430,156,'submit(assignment, project)',22)
  d.rect(765,215,310,57);d.text(920,252,'Submission accepted',22)
  d.arrow(730,290,420,340,RED);d.text(540,290,'reply',22,color=RED)
  d.text(395,355,'×',40,color=RED);d.text(490,378,'reply lost',22,color=RED)
 else:
  d.arrow(190,155,480,205,RED);d.text(395,151,'submit(assignment, project)',22)
  d.text(505,223,'×',40,color=RED);d.text(530,260,'request lost',22,color=RED)
  d.text(910,322,'No submission accepted',22)
 d.text(190,477,'Timeout: no reply received',24,color=RED,weight='bold')
 d.save(name)
# Timeout SVGs are now editable masters; regenerate PDFs with just headless-preview.
print('Created six diagrams as SVG and PDF.')

# Delivery analogy: time for one trip, transport capacity, completed work.
d=Diagram(h=460)
def truck(x,y):
 d.rect(x,y,95,55,LIGHT,BLUE)
 d.rect(x+95,y+20,42,35,'#fff0dc',ORANGE)
 for cx in [x+25,x+112]:
  d.items.append(f'<circle cx="{cx}" cy="{y+59}" r="11" fill="{INK}"/>')
def parcel(x,y):
 d.rect(x,y,35,32,'#fff0dc',ORANGE)
 d.line(x+17,y,x+17,y+32,ORANGE,2)
for x,title in [(10,'Latency'),(385,'Bandwidth'),(760,'Throughput')]:
 d.rect(x,15,350,425,'#f7fafb','#c5d5df')
 d.text(x+175,60,title,27,weight='bold')
# A single truck travels from dispatch to arrival; a clock measures duration.
truck(100,130)
d.arrow(55,255,320,255)
d.text(60,287,'Dispatch',19,anchor='start')
d.text(318,287,'Arrival',19,anchor='end')
d.items.append(f'<circle cx="280" cy="140" r="29" fill="white" stroke="{BLUE}" stroke-width="3"/>')
d.line(280,140,280,121,BLUE,3);d.line(280,140,294,150,BLUE,3)
d.text(185,344,'Time for one delivery',22,weight='bold')
d.text(185,380,'Request → result: seconds',20)
# Cargo can pass through a route only up to its capacity.
for row in range(2):
 d.line(420,135+row*75,700,135+row*75,BLUE,3)
 for j in range(4):parcel(435+j*57,148+row*75)
d.arrow(430,295,695,295)
d.text(560,344,'Maximum cargo per second',22,weight='bold')
d.text(560,380,'Link capacity: bits/second',20)
# Finished deliveries count as throughput, not just arriving at the depot.
truck(795,143)
for y in [125,185,245]:
 parcel(1000,y)
 d.line(1050,y+16,1057,y+24,BLUE,3);d.line(1057,y+24,1075,y+4,BLUE,3)
d.text(935,316,'Completed deliveries',22,weight='bold')
d.text(935,348,'per second',22,weight='bold')
d.text(935,389,'Accepted projects/second',20)
# latency-bandwidth-throughput.svg is the editable master; use just headless-preview.
print('Created delivery analogy as SVG and PDF.')
