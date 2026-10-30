"""Orientation visuals adapted from the Web Applications lecture 00; bilingual, no external artwork."""
from pathlib import Path
from html import escape
import subprocess
D=Path(__file__).resolve().parent
DARK='#18344b'; GRAY='#546573'; LINE='#d4e3ec'
def svg(name,body,w=100,h=100):
 p=D/(name+'.svg');p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'+body+'</svg>')
 subprocess.run(['rsvg-convert','-f','pdf','-o',str(p.with_suffix('.pdf')),str(p)],check=True)
def t(x,y,v,size=22,color=DARK,weight=400,anchor='start'):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(v)}</text>'

# Original simplified visual identifiers; not official logo files.
svg('tech-python','<path d="M49 5 C28 5 29 14 29 14 V25 H51 V29 H20 C8 29 5 40 5 50 C5 62 9 70 20 70 H28 V58 C28 49 35 44 44 44 H62 C70 44 71 38 71 33 V16 C71 9 64 5 49 5Z" fill="#3776ab"/><path d="M51 95 C72 95 71 86 71 86 V75 H49 V71 H80 C92 71 95 60 95 50 C95 38 91 30 80 30 H72 V42 C72 51 65 56 56 56 H38 C30 56 29 62 29 67 V84 C29 91 36 95 51 95Z" fill="#ffd43b"/><circle cx="39" cy="15" r="4" fill="#fff"/><circle cx="61" cy="85" r="4" fill="#fff"/>')
svg('tech-asyncio','<rect x="5" y="5" width="90" height="90" rx="16" fill="#e4eff7"/><path d="M72 36 A26 26 0 1 0 75 58" fill="none" stroke="#3886ad" stroke-width="5" stroke-linecap="round"/><path d="M63 34 L74 36 L76 24" fill="none" stroke="#3886ad" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'+t(50,57,'await',15,'#2d6688',700,'middle'))
svg('tech-fastapi','<circle cx="50" cy="50" r="45" fill="#059486"/><path d="M56 14 L28 56 H48 L42 86 L72 42 H52Z" fill="#fff"/>')
svg('tech-docker','<g fill="#1d63ed"><rect x="18" y="38" width="13" height="12" rx="1.5"/><rect x="33" y="38" width="13" height="12" rx="1.5"/><rect x="48" y="38" width="13" height="12" rx="1.5"/><rect x="33" y="24" width="13" height="12" rx="1.5"/><rect x="48" y="24" width="13" height="12" rx="1.5"/><rect x="63" y="38" width="13" height="12" rx="1.5"/><rect x="48" y="10" width="13" height="12" rx="1.5"/><path d="M6 54 H82 C86 46 91 44 96 46 C93 50 92 53 88 55 C80 78 60 90 36 90 C18 90 8 78 6 54Z"/></g><circle cx="26" cy="68" r="3" fill="#fff"/>')

for lang in ['hr','en']:
 def tr(hr,en):return hr if lang=='hr' else en
 # Fictional repository history; dates illustrate a few commits a week over three weeks.
 body=f'<rect x="1" y="1" width="1038" height="358" rx="16" fill="#fff" stroke="{LINE}"/><path d="M1 55 H1039" stroke="{LINE}"/>'
 body+=t(24,36,tr('projekt / Povijest commitova','project / Commit history'),24,weight=700)+t(1016,36,tr('Ilustrativni primjer · nekoliko commitova tjedno, 3 tjedna','Illustrative example · a few commits a week, 3 weeks'),18,'#637585',anchor='end')
 rows=[('Ana','A',tr('Dodaje FastAPI uslugu za predaju','Adds the FastAPI submission service'),tr('3. 11.','3 Nov'),'a31f902','#dceef9'),
  ('Marko','M',tr('Šalje obavijest asinkrono','Sends the notification asynchronously'),tr('5. 11.','5 Nov'),'b62e140','#e3f2e8'),
  ('Iva','I',tr('Dodaje Docker Compose konfiguraciju','Adds the Docker Compose configuration'),tr('10. 11.','10 Nov'),'c83a215','#f1e8fa'),
  ('Ana','A',tr('Dodaje istek vremena čekanja','Adds a request timeout'),tr('12. 11.','12 Nov'),'d94b326','#dceef9'),
  ('Marko','M',tr('Sprječava dvostruku predaju','Prevents duplicate submissions'),tr('17. 11.','17 Nov'),'e15c437','#e3f2e8'),
  ('Ana','A',tr('Bilježi ispade usluge u log','Logs service failures'),tr('20. 11.','20 Nov'),'f26d548','#dceef9')]
 for i,(name,initial,msg,date,sha,color) in enumerate(rows):
  y=83+i*44
  body+=f'<circle cx="38" cy="{y-6}" r="15" fill="{color}"/>'+t(38,y,initial,16,weight=700,anchor='middle')+t(65,y,name,18,weight=700)+t(140,y,msg,18)+t(520,y,date,16,'#637585')+t(590,y,sha,16,'#637585')
 body+=f'<path d="M681 71 V333" stroke="{LINE}"/>'+t(711,91,tr('Commitovi po autoru','Commits by author'),20,weight=700)
 for i,(name,count,color) in enumerate([('Ana',3,'#3886ad'),('Marko',2,'#58a074'),('Iva',1,'#9d7abe')]):
  y=132+i*65
  body+=t(711,y,name,20)+t(1001,y,str(count),20,weight=700,anchor='end')+f'<rect x="711" y="{y+10}" width="290" height="10" rx="5" fill="#edf2f6"/><rect x="711" y="{y+10}" width="{count*90}" height="10" rx="5" fill="{color}"/>'
 svg(f'github-history.{lang}',body,1040,360)

 # Working days counted forward from submission; example without public holidays.
 body=t(22,31,tr('Primjer: predaja u petak → obrana najranije u srijedu','Example: Friday submission → defence on Wednesday at the earliest'),24,weight=700)
 days=[(tr('PET','FRI'),tr('PREDAJA','SUBMIT'),tr('predaja projekta','project submitted'),'#dfedf5',24),
  (tr('SUB','SAT'),'—',tr('ne broji se','not counted'),'#f0f1f3',34),
  (tr('NED','SUN'),'—',tr('ne broji se','not counted'),'#f0f1f3',34),
  (tr('PON','MON'),'1',tr('radni dan','working day'),'#e7f2eb',34),
  (tr('UTO','TUE'),'2',tr('radni dan','working day'),'#e7f2eb',34),
  (tr('SRI','WED'),'3',tr('obrana','defence'),'#dfedf5',34)]
 for i,(day,count,label,color,size) in enumerate(days):
  x=22+i*169
  body+=f'<rect x="{x}" y="61" width="151" height="151" rx="14" fill="{color}"/>'
  body+=t(x+16,91,day,20,weight=700)+t(x+16,148,count,size,weight=700)+t(x+16,190,label,17)
 body+=t(22,253,tr('Brojimo od predaje: ponedjeljak 1 → utorak 2 → srijeda 3.','Count from submission: Monday 1 → Tuesday 2 → Wednesday 3.'),22)
 body+=t(22,287,tr('Subotu i nedjelju preskačemo. Primjer je bez blagdana.','Saturday and Sunday are skipped. The example has no public holidays.'),20,'#637585')
 svg(f'submission-calendar.{lang}',body,1040,310)

 # Dates supplied by the lecturer for the Web Applications deck and confirmed for this course on 2026-10-12.
 body='<rect width="1040" height="210" fill="white"/>'
 for x,accent,bg,date,title,detail in [
  (10,'#ad7840','#fcf5e9',tr('20. 7. – 25. 8.','20 Jul – 25 Aug'),tr('Godišnji odmor nastavnika','Lecturer annual leave'),tr('Planirajte komunikaciju i završetak projekta.','Plan communication and project completion.')),
  (540,'#3886ad','#f3f8fb',tr('30. 9.','30 Sep'),tr('Završetak akademske godine','End of the academic year'),tr('Projekt treba obraniti u tekućoj ak. godini.','Defend within the current academic year.'))]:
  body+=f'<rect x="{x}" y="12" width="490" height="180" rx="16" fill="{bg}" stroke="{LINE}"/>'
  body+=f'<rect x="{x+22}" y="37" width="42" height="40" rx="6" fill="none" stroke="{accent}" stroke-width="2.5"/><path d="M{x+22} 49 H{x+64} M{x+32} 31 V42 M{x+54} 31 V42" fill="none" stroke="{accent}" stroke-width="2.5" stroke-linecap="round"/>'
  body+=t(x+83,68,date,32,accent,700)+t(x+22,116,title,25,weight=700)+t(x+22,156,detail,20,GRAY)
 svg(f'academic-year.{lang}',body,1040,210)
