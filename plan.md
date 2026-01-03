# Plán pro řešení build chyb OpenKomodoIDE

## Úvod

Tento dokument popisuje plán pro identifikaci a řešení build chyb v projektu OpenKomodoIDE po migraci z Python 2 na Python 3 a z Firefox 35 na Firefox 140 ESR.

## Aktuální stav

- **Python 3 migrace**: Dokončena - build.py podporuje Python 3.11
- **Firefox 140 ESR podpora**: Připravena - patchy jsou vytvořeny a dokumentovány
- **Build systém**: Modernizován pro podporu nových verzí

## Hlavní komponenty

1. **mozilla/build.py**: Hlavní build skript s podporou Python 3 a Firefox 140 ESR
2. **Patch systém**: Kompletní sada 7 patchů pro různé platformy a architektury
3. **Konfigurace**: Podpora pro moderní build systémy

## Identifikované potenciální problémy

1. **Patch aplikace**: Některé patchy (např. confvars.sh) mohou vyžadovat manuální zásah
2. **Platform-specifické problémy**: Různé platformy mohou mít specifické build problémy
3. **Závislosti**: Moderní build systémy vyžadují nové verze nástrojů

## Fáze řešení

### Fáze 1: Analýza a diagnostika (Aktuálně probíhá)

**Cíl**: Identifikovat konkrétní build chyby

**Úkoly**:
- [x] Prozkoumat build logy pro identifikaci konkrétních chyb
- [ ] Testovat build proces na různých platformách
- [ ] Identifikovat specifické chyby v kódu nebo konfiguraci

**Očekávaný výstup**: Seznam konkrétních chyb s prioritou

### Fáze 2: Oprava identifikovaných chyb

**Cíl**: Opravit všechny identifikované build chyby

**Úkoly**:
- [ ] Opravit problémy s patchy (např. confvars.sh)
- [ ] Aktualizovat build konfiguraci pro moderní systémy
- [ ] Opravit platform-specifické problémy (Windows, Linux, macOS)
- [ ] Vyřešit problémy s závislostmi

**Očekávaný výstup**: Funkční build systém bez kritických chyb

### Fáze 3: Testování a validace

**Cíl**: Ověřit, že všechny chyby jsou opraveny

**Úkoly**:
- [ ] Otestovat opravený build na všech podporovaných platformách
- [ ] Validovat funkčnost všech komponent
- [ ] Zajistit kompatibilitu s Firefox 140 ESR
- [ ] Provést regresní testy

**Očekávaný výstup**: Validovaný build proces na všech platformách

### Fáze 4: Dokumentace

**Cíl**: Aktualizovat dokumentaci pro vývojáře

**Úkoly**:
- [ ] Aktualizovat dokumentaci s novými build instrukcemi
- [ ] Dokumentovat změny a řešení problémů
- [ ] Vytvořit průvodce pro vývojáře
- [ ] Aktualizovat README a další dokumentační soubory

**Očekávaný výstup**: Kompletní a aktuální dokumentace

## Konkrétní akční plán

### 1. Spuštění testovacího buildu

```bash
# Spustit testovací build
python3 test_build.py

# Spustit build s detekcí platformy
python3 mozilla/build.py configure -k 12.0 --python-version=3.11
python3 mozilla/build.py all
```

### 2. Analýza build logů

- Prozkoumat výstup test_build.py
- Identifikovat konkrétní chyby v build procesu
- Zaznamenat všechny chyby do deníku

### 3. Oprava problémů

**Priorita 1 - Kritické chyby**:
- Chyby bránící kompletnímu buildu
- Patch aplikace problémy
- Závislosti problémy

**Priorita 2 - Platform-specifické problémy**:
- Windows-specifické chyby
- Linux-specifické chyby
- macOS-specifické chyby

**Priorita 3 - Konfigurační problémy**:
- Build konfigurace
- Environment proměnné
- Nástrojové řetězce

### 4. Testování

```bash
# Test na Linuxu
python3 test_build.py

# Test na macOS
python3 test_build.py

# Test na Windows
python3 test_build.py
```

### 5. Dokumentace

- Aktualizovat README.md
- Aktualizovat BUILD.md
- Vytvořit průvodce řešením problémů

## Očekávané výstupy

1. **Funkční build systém** pro Python 3 a Firefox 140 ESR
2. **Opravené build chyby** s dokumentovanými řešeními
3. **Aktualizovaná dokumentace** pro vývojáře
4. **Validovaný build proces** na všech platformách

## Časový plán

| Fáze | Očekávaná doba | Priorita |
|------|---------------|----------|
| Analýza | 1-2 dny | Vysoká |
| Oprava chyb | 3-5 dní | Vysoká |
| Testování | 2-3 dny | Střední |
| Dokumentace | 1-2 dny | Nízká |

## Metriky úspěchu

- ✅ Build úspěšně dokončen na všech platformách
- ✅ Všechny testy projít
- ✅ Dokumentace aktualizována
- ✅ Žádné kritické chyby v build procesu

## Rizika a mitigace

| Riziko | Mitigace |
|-------|----------|
| Platform-specifické problémy | Testovat na všech platformách |
| Patch aplikace problémy | Připravit manuální instrukce |
| Závislosti problémy | Dokumentovat požadavky |
| Časové omezení | Prioritizovat kritické problémy |

## Závěr

Tento plán zajistí systematické řešení build problémů a úspěšnou migraci na moderní platformu. Cílem je mít plně funkční build systém pro OpenKomodoIDE s podporou Python 3 a Firefox 140 ESR.