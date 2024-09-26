# Use cases

**CRUD**: dovoľuje create, read, update, delete s entitami

V kurzíve sú veci, u ktorých *nie je jasné či sú povinné*.

## Role

### Administrátor

> spravuje uživatele, jako jediný vytváří pečovatele a veterináře

- vidí zoznam všetkých používateľov, kde môže
  - meniť role
  - CRUD
  - *filtrovať podľa mena (nie je to explicitne v zadaní ale príde mi to užitočné, pokiaľ je v systéme 100+ používateľov)* 

### Pečovatel

> spravuje zvířata, vede jejich evidenci

- zoznam zvierat s možnosťami vyhľadávania a filtrácie
- CRUD so zvieratami
- evidencia ... zoznam udalostí spojených s istým zvieraťom (CRUD):
  - `venčenie`
  - `požiadavka na veterinára/vyšetrenie`
  - `iné` (informace o nalezení)

> vytváří rozvrhy pro venčení

- rozvrh časov venčenia (napr. *prehľad dňa alebo týždňa*), inými slovami pohľad len na udalosti typu `venčenie`

> ověřuje dobrovolníky

- spravuje dobrovoľníkov, podobný zoznam používateľov ako u administrátora ale pracuje len s používateľmi `Dobrovoľník`

> schvaluje rezervace zvířat na venčení, eviduje zapůjčení a vrácení

- čas venčenia, ktorý je v stave `zarezervovaný dobrovoľníkom` môže byť zmenený na stav `schválené` -> `zapožičané` -> `vrátené`

> vytváří požadavky na veterináře

- vytvorenie udalosti typu `požiadavka na veterinára`, ktorú môže veterinár zmeniť na objednanie

### Veterinář

> vyřizuje požadavky od pečovatele (plánuje vyšetření zvířat dle požadavků)

- mení stav udalosti vyšetrenie z `požiadavka od pečovatele` na `objednaný` (špecifikuje čas) a na `vybavené` (text - výsledok)

> udržuje zdravotní záznamy zvířat

- vidí prehľad udalostí typu vyšetrenie

### Dobrovolník

> rezervuje zvířata na venčení

- môže si rozkliknúť rozvrh venčenia zvieraťa
- v rozvrhu môže rezervovať/zrušiť časy venčenia

> vidí historii svých venčení

- zoznam minulých venčení (*prípadne nadchádzajúcich*)

### Neregistrovaný uživatel

> prochází informace o útulku a zvířatech

- vidí len zvieratá a ich základný popis (nevidí udalosti venčení,vyšetrení, ...)


### Každý registrovaný používateľ

- *zmeniť heslo*
- *zadať/zmeniť kontaktné informácie*
