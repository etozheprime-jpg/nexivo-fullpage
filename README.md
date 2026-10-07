# Nexivo.sbs — svetainė

Statinė, greita svetainė (HTML + CSS + JS be karkasų). Vienas `index.html`, jokio build serveryje.
Kalbos: LT (numatyta), RU, EN — perjungiama be perkrovimo, `?lang=ru` / `?lang=en` nuorodos.

## Paleidimas (5 min)
Įkelkite **`dist/`** aplanko turinį į bet kurį statinį hostingą:
- **GitHub Pages**: repo → įkelkite `dist/` turinį į šaknį → Settings → Pages → Custom domain `nexivo.sbs`.
- **Netlify / Cloudflare Pages**: nutempkite `dist/` aplanką, prijunkite domeną.

## Užklausų formos (būtina prieš paleidimą)
1. Užsiregistruokite https://web3forms.com su `hello@nexivo.sbs` — gausite nemokamą raktą.
2. `src/app.js` → `CONFIG.web3formsKey: "jūsų-raktas"` → `python3 src/build.py`.
Kol raktas tuščias, forma atidaro lankytojo el. pašto programą su paruoštu laišku (veikia, bet mažiau patogu).

## Ką redaguoti
| Ką | Kur |
|---|---|
| Visi tekstai LT/RU/EN | `src/content.py` (raktas → LT, RU, EN) |
| Maketas | `src/template.html` |
| Stilius / spalvos | `src/styles.css` (`:root` kintamieji) |
| Logika, Spin prizai | `src/app.js` (`PRIZES`) |
| Paslaugų / sprendimų / darbų sąrašai, JSON-LD | `src/build.py` |
| Soc. tinklų nuorodos | `src/template.html` (footer, `href="#"`) |
| Analitika (tik po sutikimo) | `src/app.js` → `loadAnalytics()` |

Po pakeitimų: `python3 src/build.py` → atnaujinamas `dist/index.html` ir `preview.html`.
Naujos paslaugos pridėjimas: įrašykite `s13.t/.d/.c` į `content.py` ir eilutę į `SERVICES` `build.py`.

## Prieš paleidimą patikrinkite
- Privatumo ir slapukų politikos tekstai yra šablonai — peržiūrėkite su teisininku, įrašykite duomenų valdytojo rekvizitus.
- DUK terminai (1–2 / 2–4 savaitės) ir paketų turinys — pakoreguokite pagal realią praktiką.
- Google Search Console: pridėkite domeną ir pateikite `sitemap.xml`.
