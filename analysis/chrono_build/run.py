import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib, sources, people, events
# sources whose headline was not captured verbatim: flag as descriptive
DESC = {"src:afp-2026-11-10-retornos","src:afp-2026-11-11-devolucion","src:efe-2026-11-07-prision-pena","src:gfmag-2026-11-12-fgd","src:hoy-2026-11-04-denuncia-bcp","src:elnacional-2026-11-19-rey-rompe-silencio","src:telex-2026-11-03-otp","src:ueno-2026-06-03-otp","src:ueno-2026-08-06-triodos-gawa","src:riotimes-2026-11-11-benitez","src:riotimes-2026-11-07-charges","src:5dias-2026-11-18-especial-ueno","src:elnacional-2026-11-10-agravan-cargos","src:dw-2026-11-17-rolon","src:europapress-2026-11-17-rolon"}
for s in lib.SOURCES:
    if s["id"] in DESC: s["title"] += " [descriptive title; headline not captured verbatim]"
used={r['prov']['source'] for rows in (lib.EVENTS,lib.ENTITIES,lib.ROLES,lib.ACCUSED) for r in rows}
lib.SOURCES[:]=[x for x in lib.SOURCES if x['id'] in used]
lib.dump()
