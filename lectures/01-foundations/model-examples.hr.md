# Radni nacrt: modeli sustava

## Infrastrukturne pretpostavke i napredak

Pretpostavke razrađujemo kroz mrežu, čvorove i vrijeme. Počinjemo prerezanim kabelom: oporavlja li se komunikacija ili ostaje prekinuta? Ponovni pokušaji pomažu samo ako neki kasniji pokušaj može stići do primatelja. Zatim razmatramo ponašanje čvorova i vremenske granice.

Možemo li obećati da će svaka valjana predaja na kraju biti prihvaćena ako struja ostane isključena, disk otkaže bez preostale obnovljive kopije ili prerezani kabel ostavi servis trajno odspojenim? Tvrdnje ovise o pretpostavkama o napajanju, pohrani, komunikaciji i oporavku. Zaustavljen sustav može izbjegavati duplikate, ali ne ostvaruje napredak. Privremeni kvar ne isključuje eventualni napredak ako se sustav oporavi i posao ostane sačuvan ili se ponovi.

## Sigurnost i napredovanje u različitim sustavima

- Plaćanje: ponovni pokušaji ne terete kupca dvaput za isto plaćanje; valjano odobreno plaćanje na kraju se dovršava.
- Rezervacija sjedala: isto sjedalo za isti događaj nije istodobno potvrđeno dvama kupcima; svaki zahtjev na kraju dobiva potvrdu ili odbijenicu.
- Red poslova: posao se ne označava dovršenim prije uspješnog izvršavanja; svaki valjani posao na čekanju na kraju se obrađuje.
- Raspodijeljeno zaključavanje: najviše jedan proces istodobno izvršava zaštićenu kritičnu sekciju; svaki ispravan proces koji nastavlja tražiti zaključavanje na kraju ga dobiva.

Za napredak pretpostavljamo oporavak servisa, uspješnu komunikaciju, očuvanje ili ponavljanje posla i pravedno raspoređivanje. Kod zaključavanja dodatno pretpostavljamo da kritične sekcije završavaju i da je moguć siguran oporavak nakon pada vlasnika.

## Ponovni pokušaj može se preklapati s izvornim zahtjevom

Klijent prestaje čekati, ali poslužitelj možda još radi. Šaljemo pokušaj A, istječe rok čekanja, šaljemo pokušaj B. Oba mogu obrađivati istu namjeravanu predaju. Primamljivo pravilo glasi: ako prihvaćeni zapis ne postoji, stvori ga. Što ako oba pokušaja provjere prije nego što ijedan stvori zapis? Sljedeći dijagram pokazuje problem i motivira invarijantu.

## Klijent je uloga, ne samo preglednik

Preglednik šalje zahtjev servisu za predaju. Servis za predaju prima taj zahtjev kao poslužitelj, ali je klijent kada poziva servis s pravilima zadatka. Svaki pozivatelj može postaviti rok čekanja za svoj poziv kako ne bi čekao beskonačno. Istek roka završava čekanje, ali sam po sebi ne zaustavlja udaljeni rad i ne otkriva njegov ishod. Rokovi nisu automatski usklađeni između slojeva.

## Povijest C: pad poslužiteljskog procesa

Zahtjev stiže i predaja se trajno pohranjuje. Proces zatim pada prije slanja odgovora. Pretpostavljamo da trajni zapis ostaje sačuvan. Preglednik ne dobiva odgovor prije isteka čekanja. Pad prije pohrane mogao bi dati drukčiji ishod; sam timeout ne otkriva kada je proces pao. U nekim izvođenjima transport može ranije prijaviti prekid veze.

## Podsjetnik na Web aplikacije: TTFB

TTFB mjeri čekanje do prvog bajta odgovora, a ne preuzimanje cijelog odgovora. Ovdje brojimo od početka navigacije: DNS, TCP, TLS te prijenos zahtjeva, čekanje, obrada i prijenos prvog bajta odgovora. DNS i veza mogu se ponovno iskoristiti. Veća propusnost veze ne uklanja čekanje obrade. Prvi bajt ne dokazuje trajno prihvaćanje projekta; treba provjeriti što odgovor potvrđuje. Dijagram je shematski primjer nove HTTPS veze preko TCP-a.

## Raspodijeljeni sustav ili ne?

Preglednik, API i baza kao zasebni procesi na istom računalu surađuju porukama radi obrade zahtjeva. Zadovoljavaju našu definiciju, ali dijele kvar fizičkog računala. Računala koja renderiraju različite kadrove istog filma koordiniraju zajednički posao. Nepovezana prijenosna računala na istoj Wi-Fi mreži nemaju nužno zajednički cilj. Dretve koje koriste samo zajedničku memoriju ne zadovoljavaju kriterij komunikacije porukama iz naše definicije. API i radni proces u kontejnerima na istom računalu zadovoljavaju našu definiciju ako koordiniraju porukama, ali dijele kvar fizičkog računala.

Tri MPI procesa računaju prosječnu temperaturu: proces 0 dijeli mjerenja u tri dijela, zadržava jedan i šalje ostale procesima 1 i 2. Svaki računa lokalni zbroj i broj mjerenja. Radni procesi šalju rezultate procesu 0, koji ukupni zbroj dijeli ukupnim brojem mjerenja. Mogu raditi na jednom ili više računala.

## Primjeri okruženja

- WWW: preglednik i udaljeni API; nema pouzdane granice vremena odgovora, veze se prekidaju, poslužitelji se ponovno pokreću. Klijenti nisu nužno pouzdani.
- Jedno računalo: API i radni proces komuniciraju lokalno. Običan OS ne jamči vremensku granicu; pad računala utječe na oba procesa.
- LAN: mala tipična kašnjenja ne isključuju pauze ni mrežne particije. Za pouzdane poslužitelje možemo odabrati model pada i oporavka.

Za napredak algoritma po potrebi dodatno pretpostavljamo eventualni oporavak i stabilne vremenske granice. LAN i localhost sami po sebi ne jamče sinkronost. To su izbori modela, a ne jamstva izvedena samo iz mjesta izvođenja.

Model sustava pojednostavljen je opis ponašanja komponenti i mreže te jamstava na koja se algoritam smije osloniti.

Algoritam iznosi tvrdnje o ispravnosti. Svaka tvrdnja mora vrijediti u svim izvođenjima dopuštenima navedenim pretpostavkama modela. Primjer: ponovljeni pokušaji nikad ne stvaraju dva prihvaćena zapisa iste predaje, čak ni nakon ponovnog pokretanja servisa. Model sam ne osigurava tu tvrdnju; potrebno ju je opravdati algoritmom i njegovim pretpostavkama. Tvrdnja o eventualnom prihvaćanju dodatno zahtijeva oporavak servisa, uspješnu komunikaciju, očuvanje ili ponavljanje posla te njegovo eventualno izvršavanje.

Primjer portala: poruke mogu kasniti ili se izgubiti; servis može pasti i ponovno se pokrenuti; ne pretpostavljamo najveće vrijeme odgovora.

- Crash-stop: proces za predaju staje i u promatranom izvođenju više ne radi.
- Crash-recovery: proces se ponovno pokreće; prihvaćeni zapisi ostaju u trajnoj pohrani, ali red čekanja u memoriji nestaje.
- Byzantine: neispravan servis studentu javlja da je projekt prihvaćen, a nastavniku da nije.
- Sinkroni: pretpostavimo da svaka poruka između ispravnih čvorova stiže unutar 20 ms. Dolazak nakon 35 ms krši pretpostavku.
- Asinkroni: ne pretpostavljamo granicu kašnjenja. Odgovor nakon 2 s dopušten je i nakon timeouta od 1 s.
- Djelomično sinkroni: tijekom zagušenja poruke kasne 2 s. Nakon nepoznatog trenutka stabilizacije sve nove poruke između ispravnih čvorova stižu unutar 20 ms i ta granica nadalje vrijedi.

Brojevi su zamišljeni primjeri. Granica kašnjenja poruke nije granica ukupnog vremena odgovora. Pregled hrvatskog nacrta i engleskog prijevoda još nije dovršen.

## Motivacija za djelomičnu sinkronost — nacrt za pregled

Zagušenje Interneta, promjene ruta i zastoji procesa motiviraju djelomično sinkroni model. To nije jamstvo Interneta ni tvrdnja da je 99% zahtjeva brzo. Slika prikazuje eventualnu sinkronost: nakon nepoznatog konačnog trenutka stabilizacije granice vrijede do kraja izvođenja. Stvarni sustavi mogu ponovno postati nestabilni; dovoljno dugo stabilno razdoblje može omogućiti dovršetak operacije, ovisno o algoritmu i ostalim pretpostavkama. Cilj dizajna: očuvati sigurnost tijekom poremećaja i ostvariti napredak kada se uvjeti stabiliziraju. Algoritam mora opravdati te tvrdnje.

## Uvid: prekratko čekanje i agresivni ponovljeni pokušaji

Prekratki timeouti i agresivni ponovljeni pokušaji mnogih klijenata mogu izazvati oluju ponovljenih zahtjeva: više opterećenja usporava odgovore, što izaziva još ponavljanja. Izvorni zahtjevi pritom još mogu biti aktivni. Legitimni klijenti tako mogu sami prouzročiti uskraćivanje usluge s učinkom sličnim DDoS-u, bez napadača. Ograničiti broj ponavljanja i povećavati razmake uz nasumični pomak (backoff i jitter). Sigurnost ponovljenih zahtjeva ostaje zaseban zahtjev. Nacrt i prijevod čekaju pregled; izvor: AWS Builders’ Library, Timeouts, retries, and backoff with jitter.
