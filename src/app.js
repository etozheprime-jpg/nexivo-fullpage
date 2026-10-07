(() => {
"use strict";

/* ===== CONFIG =====
   Užklausų siuntimas: įrašykite Web3Forms raktą (https://web3forms.com, nemokamas).
   Jei raktas tuščias, forma atidarys lankytojo el. pašto programą su paruoštu laišku. */
const CONFIG = {
  web3formsKey: "",
  email: "hello@nexivo.sbs",
};

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch {} },
};
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const finePointer = matchMedia("(hover: hover) and (pointer: fine)").matches;
document.documentElement.classList.add("js");

/* ===== i18n ===== */
const LANGS = ["lt", "ru", "en"];
const LOCALES = { lt: "lt_LT", ru: "ru_RU", en: "en_GB" };
let lang = "lt";
const t = (k) => (I18N[lang] && I18N[lang][k]) ?? I18N.lt[k] ?? k;

function applyLang(l, save = true) {
  lang = LANGS.includes(l) ? l : "lt";
  document.documentElement.lang = lang;
  $$("[data-t]").forEach((el) => { el.textContent = t(el.dataset.t); });
  $$("[data-th]").forEach((el) => { el.innerHTML = t(el.dataset.th); });
  $$("[data-tp]").forEach((el) => { el.placeholder = t(el.dataset.tp); });
  $$("[data-ta]").forEach((el) => { el.setAttribute("aria-label", t(el.dataset.ta)); });
  $$("[data-tl]").forEach((el) => {
    el.innerHTML = t(el.dataset.tl).split("|").map((x) => `<li>${x}</li>`).join("");
  });
  document.title = t("meta.title");
  $("#meta-desc").content = t("meta.desc");
  $("#og-title").content = t("meta.title");
  $("#og-desc").content = t("meta.desc");
  $("#og-locale").content = LOCALES[lang];
  $$(".lang button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === lang)));
  if (save) {
    store.set("nexivo_lang", lang);
    const u = new URL(location.href);
    if (lang === "lt") u.searchParams.delete("lang"); else u.searchParams.set("lang", lang);
    history.replaceState(null, "", u);
  }
  refreshSpinLabels();
}
$$(".lang button").forEach((b) => b.addEventListener("click", () => applyLang(b.dataset.lang)));

/* ===== header / menu ===== */
const hdr = $("#hdr");
const onScrollHeader = () => {
  hdr.classList.toggle("scrolled", scrollY > 8);
  document.body.classList.toggle("scrolled-away", scrollY > 40);
};
const burger = $("#burger");
function setMenu(open) {
  document.body.classList.toggle("menu-open", open);
  burger.setAttribute("aria-expanded", String(open));
  document.body.style.overflow = open ? "hidden" : "";
}
burger.addEventListener("click", () => setMenu(!document.body.classList.contains("menu-open")));
$$("#nav a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });
matchMedia("(min-width:1080px)").addEventListener("change", () => setMenu(false));

/* ===== hero pipeline ===== */
const pipe = $("#pipe");
const DUR = 3400;
let step = 0, pipeTimer = null;
function setStep(n) {
  step = n;
  pipe.dataset.step = n;
  $$(".pipe-tabs button", pipe).forEach((b) => {
    const on = Number(b.dataset.step) === n;
    b.setAttribute("aria-selected", String(on));
    const i = $("i", b); i.style.animation = "none"; void i.offsetWidth; i.style.animation = "";
  });
}
function runPipe() {
  clearInterval(pipeTimer);
  if (reduced) return;
  pipe.style.setProperty("--dur", DUR + "ms");
  pipeTimer = setInterval(() => setStep((step + 1) % 3), DUR);
}
$$(".pipe-tabs button", pipe).forEach((b) => b.addEventListener("click", () => { setStep(Number(b.dataset.step)); runPipe(); }));
pipe.addEventListener("pointerenter", () => { if (finePointer) { clearInterval(pipeTimer); pipe.classList.add("paused"); } });
pipe.addEventListener("pointerleave", () => { if (finePointer) { pipe.classList.remove("paused"); runPipe(); } });
if (reduced) $$(".pipe-tabs i").forEach((i) => (i.style.display = "none"));
setStep(0); runPipe();

/* ===== spin ===== */
const PRIZES = [
  { k: "p1", ic: "percent", c: "#3d63f8" },
  { k: "p2", ic: "percent", c: "#5b4cf7" },
  { k: "p3", ic: "search", c: "#14b8fc" },
  { k: "p4", ic: "message", c: "#22d3ee" },
  { k: "p5", ic: "gauge", c: "#38bdf8" },
  { k: "p6", ic: "map", c: "#6d5bff" },
  { k: "p7", ic: "layout", c: "#8b1cf6" },
  { k: "p8", ic: "bulb", c: "#a855f7" },
];
const SPIN_KEY = "nexivo_spin";
const strip = $("#strip"), spinBtn = $("#spinBtn"), win = $(".case-win");
const CARD = 156, GAP = 12, WIN_INDEX = 46, TOTAL = 54;
let winnerIdx = WIN_INDEX, spinning = false, jitter = 0;

const rnd = (n) => { const a = new Uint32Array(1); crypto.getRandomValues(a); return a[0] % n; };
const prizeCard = (p, i) =>
  `<div class="prize" data-i="${i}" style="--c:${p.c}"><svg class="i"><use href="#i-${p.ic}"/></svg><span data-t="${p.k}">${t(p.k)}</span></div>`;

function buildStrip(finalPrize) {
  const items = [];
  for (let i = 0; i < TOTAL; i++) items.push(PRIZES[rnd(PRIZES.length)]);
  // keep the visible start varied
  for (let i = 0; i < PRIZES.length; i++) items[i] = PRIZES[(i * 3) % PRIZES.length];
  if (finalPrize) items[WIN_INDEX] = finalPrize;
  strip.innerHTML = items.map(prizeCard).join("");
}
function offsetFor(index, j = 0) {
  return index * (CARD + GAP) + CARD / 2 - win.clientWidth / 2 + j;
}
function idleOffset() {
  strip.style.transition = "none";
  strip.style.transform = `translateX(${-offsetFor(4)}px)`;
}
function refreshSpinLabels() {
  const saved = store.get(SPIN_KEY);
  $("#oddsList").innerHTML = PRIZES.map((p) => `<li><svg class="i" style="color:${p.c}"><use href="#i-${p.ic}"/></svg>${t(p.k)}</li>`).join("");
  if (saved) $("#spinPrize").textContent = t(saved);
  const lbl = $("span", spinBtn);
  if (spinning) lbl.textContent = t("spin.spinning");
  else if (saved) lbl.textContent = t("spin.done");
  else lbl.textContent = t("spin.btn");
  if ($("#winModal").open && saved) $("#winPrize").textContent = t(saved);
}
function showSaved(key) {
  const p = PRIZES.find((x) => x.k === key);
  buildStrip(p);
  strip.style.transition = "none";
  strip.style.transform = `translateX(${-offsetFor(WIN_INDEX)}px)`;
  strip.children[WIN_INDEX].classList.add("win");
  spinBtn.disabled = true;
  $("#spinResult").hidden = false;
  refreshSpinLabels();
}
function spin() {
  if (spinning || store.get(SPIN_KEY)) return;
  spinning = true;
  const prize = PRIZES[rnd(PRIZES.length)]; // fair: chosen up front, equal 1/8 chance, animation lands on it
  store.set(SPIN_KEY, prize.k); // saved immediately so a reload can't re-roll
  buildStrip(prize);
  idleOffset();
  spinBtn.disabled = true;
  refreshSpinLabels();
  jitter = (rnd(1000) / 1000 - 0.5) * CARD * 0.7;
  void strip.offsetWidth;
  const ms = reduced ? 10 : 6200;
  strip.style.transition = `transform ${ms}ms cubic-bezier(.12,.62,.08,1)`;
  strip.style.transform = `translateX(${-offsetFor(WIN_INDEX, jitter)}px)`;
  const done = () => {
    strip.removeEventListener("transitionend", done);
    spinning = false;
    strip.style.transition = "transform .5s cubic-bezier(.2,.7,.2,1)";
    strip.style.transform = `translateX(${-offsetFor(WIN_INDEX)}px)`;
    strip.children[WIN_INDEX].classList.add("win");
    $("#spinResult").hidden = false;
    refreshSpinLabels();
    navigator.vibrate?.(30);
    setTimeout(openWin, reduced ? 0 : 650);
  };
  if (reduced) setTimeout(done, 20); else strip.addEventListener("transitionend", done);
}
spinBtn.addEventListener("click", spin);
addEventListener("resize", () => {
  if (spinning) return;
  const saved = store.get(SPIN_KEY);
  strip.style.transition = "none";
  strip.style.transform = `translateX(${-(saved ? offsetFor(WIN_INDEX) : offsetFor(4))}px)`;
});
const saved0 = store.get(SPIN_KEY);
if (saved0) setTimeout(() => showSaved(saved0)); else { buildStrip(); requestAnimationFrame(idleOffset); }

function openWin() {
  const k = store.get(SPIN_KEY); if (!k) return;
  $("#winPrize").textContent = t(k);
  $("#winModal").showModal();
}
$("#claimAgain").addEventListener("click", openWin);

/* ===== dialogs ===== */
$$("dialog").forEach((d) => {
  d.addEventListener("click", (e) => { if (e.target === d || e.target.closest("[data-close]")) d.close(); });
});
function openPolicy(which) {
  $("#pol-h").textContent = t(which === "cookies" ? "ft.cookies" : "ft.privacy");
  $("#polBody").innerHTML = t(which === "cookies" ? "pol.cookies" : "pol.privacy");
  $("#polModal").showModal();
}
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-policy]");
  if (b) { e.preventDefault(); openPolicy(b.dataset.policy); }
});
if (location.hash === "#privatumo-politika") openPolicy("privacy");
if (location.hash === "#slapuku-politika") openPolicy("cookies");
function showResult(kind) {
  const m = $("#okModal");
  $("#ok-h").textContent = t(kind === "mail" ? "mail.h" : "ok.h");
  $("#ok-p").textContent = t(kind === "mail" ? "mail.p" : "ok.p");
  m.showModal();
}

/* ===== lead sending ===== */
const NEED_KEYS = { web: "need.web", landing: "need.landing", shop: "need.shop", ai: "need.ai", bot: "need.bot", crm: "need.crm", auto: "need.auto", other: "need.other" };
async function sendLead(data, subject) {
  if (data.botcheck) return "sent";
  delete data.botcheck;
  data.language = lang.toUpperCase();
  if (CONFIG.web3formsKey) {
    const r = await fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ access_key: CONFIG.web3formsKey, subject, from_name: "nexivo.sbs", ...data }),
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok || j.success === false) throw new Error("send");
    return "sent";
  }
  const body = Object.entries(data).filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`).join("\n");
  location.href = `mailto:${CONFIG.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  return "mail";
}
const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
function markInvalid(form, names) {
  $$(".invalid", form).forEach((el) => el.classList.remove("invalid"));
  names.forEach((n) => form.elements[n].classList.add("invalid"));
  if (names[0]) form.elements[names[0]].focus();
}
function formError(form, msg) { const e = $(".form-err", form); e.textContent = msg || ""; e.hidden = !msg; }

const leadForm = $("#leadForm");
leadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = leadForm.elements, bad = [];
  if (!f.name.value.trim()) bad.push("name");
  if (!emailOk(f.email.value.trim())) bad.push("email");
  if (!f.need.value) bad.push("need");
  markInvalid(leadForm, bad);
  if (bad.length) return formError(leadForm, t("f.req"));
  formError(leadForm, "");
  const btn = $("button[type=submit]", leadForm);
  btn.classList.add("loading"); btn.textContent = t("f.sending");
  const data = Object.fromEntries(new FormData(leadForm));
  data.need = t(NEED_KEYS[data.need]);
  const prize = store.get(SPIN_KEY); if (prize) data.spin_prize = I18N.lt[prize];
  try {
    const res = await sendLead(data, `Nauja užklausa: ${data.need} — ${data.name}`);
    leadForm.reset(); showResult(res);
  } catch { formError(leadForm, t("f.err")); }
  finally { btn.classList.remove("loading"); btn.textContent = t("cta.offer"); }
});
$$("input,select,textarea", leadForm).forEach((el) => el.addEventListener("input", () => el.classList.remove("invalid")));

const claimForm = $("#claimForm");
claimForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = claimForm.elements;
  const em = f.email.value.trim(), ph = f.phone.value.trim();
  const bad = [];
  if (em && !emailOk(em)) bad.push("email");
  if (!em && ph.replace(/\D/g, "").length < 6) bad.push(em ? "phone" : "email");
  markInvalid(claimForm, bad);
  if (bad.length) return formError(claimForm, t("f.contactreq"));
  formError(claimForm, "");
  const btn = $("button[type=submit]", claimForm);
  btn.classList.add("loading"); btn.textContent = t("f.sending");
  const data = Object.fromEntries(new FormData(claimForm));
  data.prize = I18N.lt[store.get(SPIN_KEY)];
  try {
    const res = await sendLead(data, `Nexivo Spin prizas: ${data.prize}`);
    claimForm.reset(); $("#winModal").close(); showResult(res);
  } catch { formError(claimForm, t("f.err")); }
  finally { btn.classList.remove("loading"); btn.textContent = t("spin.claim"); }
});

/* CTAs that preselect a need */
document.addEventListener("click", (e) => {
  const a = e.target.closest("[data-need]");
  if (!a) return;
  $("#needSel").value = a.dataset.need;
  $("#needSel").classList.remove("invalid");
  if (a.dataset.x) {
    const msg = $("#msgField");
    if (!msg.value.trim()) msg.value = t("sol.prefill") + t(a.dataset.x);
  }
  if (a.tagName === "BUTTON") $("#kontaktai").scrollIntoView({ behavior: reduced ? "auto" : "smooth" });
});

/* ===== solutions filter ===== */
$$(".filters .chip").forEach((c) => c.addEventListener("click", () => {
  $$(".filters .chip").forEach((x) => x.classList.toggle("on", x === c));
  const f = c.dataset.f;
  $$("#solList li").forEach((li) => {
    const show = f === "all" || li.dataset.cat === f;
    li.classList.toggle("hide", !show);
    li.classList.remove("pop"); if (show && !reduced) { void li.offsetWidth; li.classList.add("pop"); }
  });
}));

/* ===== service card spotlight ===== */
if (finePointer) $$(".svc-i").forEach((el) => el.addEventListener("pointermove", (e) => {
  const r = el.getBoundingClientRect();
  el.style.setProperty("--mx", e.clientX - r.left + "px");
  el.style.setProperty("--my", e.clientY - r.top + "px");
}));

/* ===== magnetic buttons ===== */
if (finePointer && !reduced) $$(".magnetic").forEach((b) => {
  b.addEventListener("pointermove", (e) => {
    const r = b.getBoundingClientRect();
    const x = (e.clientX - r.left - r.width / 2) * 0.22, y = (e.clientY - r.top - r.height / 2) * 0.35;
    b.style.transform = `translate(${x}px,${y}px)`;
  });
  b.addEventListener("pointerleave", () => { b.style.transform = ""; });
});

/* ===== reveal + counters ===== */
const io = new IntersectionObserver((ents) => ents.forEach((en) => {
  if (!en.isIntersecting) return;
  en.target.classList.add("in");
  io.unobserve(en.target);
}), { rootMargin: "0px 0px -8% 0px" });
$$(".rv").forEach((el, i) => { el.style.transitionDelay = (i % 3) * 70 + "ms"; io.observe(el); });

const countIO = new IntersectionObserver((ents) => ents.forEach((en) => {
  if (!en.isIntersecting) return;
  countIO.unobserve(en.target);
  const el = en.target, to = Number(el.dataset.to);
  if (reduced) return;
  const t0 = performance.now(), d = 1200;
  const tick = (now) => {
    const p = Math.min(1, (now - t0) / d), v = Math.round(to * (1 - Math.pow(1 - p, 3)));
    el.textContent = v;
    if (p < 1) requestAnimationFrame(tick);
  };
  el.textContent = "0";
  requestAnimationFrame(tick);
}), { threshold: 0.6 });
$$(".cnt").forEach((el) => countIO.observe(el));

/* ===== scroll: parallax orbs + sticky CTA ===== */
const orbs = $$(".hero .orb"), sticky = $("#stickyCta"), hero = $(".hero"), lead = $("#kontaktai");
let leadVisible = false, ticking = false;
new IntersectionObserver(([en]) => { leadVisible = en.isIntersecting; onScroll(); }, { threshold: 0.05 }).observe(lead);
function onScroll() {
  onScrollHeader();
  if (ticking) return; ticking = true;
  requestAnimationFrame(() => {
    const y = scrollY;
    if (!reduced && y < hero.offsetHeight) orbs.forEach((o, i) => { o.style.translate = `0 ${y * (i ? -0.08 : 0.18)}px`; });
    const cookieOpen = !$("#cookie").hidden;
    sticky.classList.toggle("show", y > hero.offsetHeight * 0.8 && !leadVisible && !cookieOpen);
    ticking = false;
  });
}
addEventListener("scroll", onScroll, { passive: true });

/* ===== full-page scroll: active section, dots, keyboard =====
   Snap itself is native CSS (scroll-snap-type on <html>); JS only syncs UI. */
const secs = $$("main > section");
const dots = $("#dots"), dotLinks = $$("a", dots), hint = $("#scrollHint");
const dotFor = new Map(secs.map((s) => [s, dotLinks.find((a) => a.hash === "#" + s.id)]));
const snapDesktop = matchMedia("(min-width:1000px) and (min-height:640px) and (hover:hover) and (pointer:fine)");
const goTo = (el) => el.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
let current = 0;
function setActive(i) {
  current = i;
  secs.forEach((s, k) => { const a = dotFor.get(s); if (a) { a.classList.toggle("on", k === i); if (k === i) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); } });
  dots.classList.toggle("on-light", secs[i].classList.contains("light"));
}
dotLinks.forEach((a) => a.addEventListener("click", (e) => {
  const target = $(a.hash); if (!target) return;
  e.preventDefault(); a.blur(); goTo(target);
}));
// active section = the one crossing the middle of the viewport (works for sections taller than the screen)
const midIO = new IntersectionObserver((ents) => ents.forEach((en) => {
  if (en.isIntersecting) setActive(secs.indexOf(en.target));
}), { rootMargin: "-50% 0px -50% 0px" });
secs.forEach((s) => midIO.observe(s));
if (!reduced) document.documentElement.classList.add("snap-fx");
const enterIO = new IntersectionObserver((ents) => ents.forEach((en) => {
  if (!en.isIntersecting) return;
  en.target.classList.add("in-view"); enterIO.unobserve(en.target);
}), { rootMargin: "0px 0px -25% 0px" });
secs.forEach((s) => enterIO.observe(s));

function stepInside(e, dy) {
  e.preventDefault();
  scrollBy({ top: dy, behavior: reduced ? "auto" : "smooth" });
}
addEventListener("keydown", (e) => {
  if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
  if (!snapDesktop.matches || document.body.classList.contains("menu-open") || $("dialog[open]")) return;
  const tg = e.target;
  if (tg.closest?.("input,textarea,select,button,summary,a[href],[contenteditable],[role=tab],dialog")) {
    if (!(tg === document.body)) return;
  }
  let to = null;
  const vh = innerHeight;
  const idx = secs.findIndex((x) => x.getBoundingClientRect().bottom > vh / 2); // section under the viewport middle
  const at = idx < 0 ? secs.length - 1 : idx, r = secs[at].getBoundingClientRect();
  switch (e.key) {
    case "ArrowDown": case "PageDown":
      if (r.bottom > vh + 8) return stepInside(e, Math.min(vh * 0.85, r.bottom - vh)); // long section: scroll inside it first
      to = secs[at + 1] || $(".ftr"); break;
    case "ArrowUp": case "PageUp":
      if (r.top < -8) return stepInside(e, -Math.min(vh * 0.85, -r.top));
      to = secs[at - 1]; break;
    case "Home": to = secs[0]; break;
    case "End": to = $(".ftr"); break;
    default: return;
  }
  e.preventDefault();
  if (to) goTo(to);
});

/* ===== cookies ===== */
const CK = "nexivo_cookies";
function loadAnalytics() {
  /* Čia įklijuokite analitikos kodą (pvz. Google Analytics / Plausible).
     Jis įkeliamas tik lankytojui paspaudus „Sutinku“. */
}
const cookie = $("#cookie");
$$("[data-ck]").forEach((b) => b.addEventListener("click", () => {
  store.set(CK, b.dataset.ck); cookie.hidden = true; onScroll();
  if (b.dataset.ck === "all") loadAnalytics();
}));
$("#cookieSettings").addEventListener("click", () => { cookie.hidden = false; onScroll(); });
const ckv = store.get(CK);
if (ckv === "all") loadAnalytics();
if (!ckv) setTimeout(() => { cookie.hidden = false; onScroll(); }, 1400);

/* ===== init language ===== */
const qLang = new URLSearchParams(location.search).get("lang");
const initLang = LANGS.includes(qLang) ? qLang : (store.get("nexivo_lang") || "lt");
if (initLang !== "lt") applyLang(initLang, false); else refreshSpinLabels();
onScroll();
})();
