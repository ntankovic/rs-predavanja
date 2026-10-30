# Stvarni sustavi: pretpostavke i jamstva

Hrvatski autorski nacrt za tri primjera prije sažetka portala. Pregled hrvatskog nacrta i engleskog prijevoda još je otvoren. Izvori su u `sources.md`. Svaki primjer ima dvije minute u planu od 60 minuta.

## etcd: samo jedan uspješan zahtjev za isto ime

etcd je replicirana pohrana ključeva i vrijednosti za koordinaciju. Tri čvora slijede protokol; mogu pasti i oporaviti se uz očuvane trajne zapise. Kašnjenja i prekidi komunikacije ne smiju narušiti sigurnost. Za napredak trebaju dva dostupna čvora i dovoljno stabilna komunikacija i obrada. Dva klijenta pokušavaju zauzeti isto ime atomskom transakcijom: ako ključ ne postoji, stvori ga. Dok ključ nije obrisan, najviše jedan pokušaj uspijeva. To je aplikacijska invarijanta izvedena iz atomskih, linearizabilnih operacija, ne jamstvo dvaju odvojenih poziva čitanja i pisanja. U podjeli 2 + 1 većina može napredovati, manjina ne može potvrditi novu promjenu.

## Cassandra: odabir razine konzistentnosti mijenja jamstva

Primjer: tri replike ćelije i obična čitanja/pisanja na razini ONE; jedna replika mora odgovoriti. Pretpostavljamo čvorove koji slijede protokol, uz padove i oporavak, promjenjiva kašnjenja i particije. Uspjeh pisanja potvrđuje traženi broj replika; ne jamči da svako sljedeće čitanje vidi tu vrijednost. Invarijanta „mjesto se proda najviše jednom” nije osigurana običnim čitaj-pa-piši postupkom. Dostupna replika omogućuje obradu, uz dovoljno resursa; konvergencija traži ponovnu komunikaciju i popravak replika. QUORUM traži većinu; za uvjetnu rezervaciju razmatraju se lake transakcije (LWT), s dodatnom koordinacijom. Ne poistovjećivati QUORUM s atomskim čitanjem i pisanjem.

## Bitcoin: valjanost lanca i vjerojatnosna konačnost

Otvorena mreža dopušta zlonamjerne sudionike. Pretpostavke uključuju sigurnu kriptografiju, prevlast poštene rudarske snage i dovoljno dobru propagaciju blokova u odnosu na rudarenje. Invarijanta: isti izlaz transakcije ne smije biti potrošen dvaput unutar jednog valjanog lanca. Dva čvora privremeno mogu pratiti različite valjane grane. Dodatne potvrde smanjuju rizik reorganizacije uz pretpostavke sigurnosnog modela; ne daju apsolutnu konačnost. Nastavak rudarenja i propagacije omogućuje rast lanca. Uključivanje konkretne transakcije traži da ostane valjana, dosegne rudare i bude odabrana; nema zajamčenog roka. U podjeli mreže grane mogu rasti zasebno, a prihvaćanje druge grane može poništiti prethodnu potvrdu.
