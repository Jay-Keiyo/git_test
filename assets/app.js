(() => {
  "use strict";

  const $ = (sel) => document.querySelector(sel);
  const state = { data: null, category: "all", query: "" };

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]
  ));

  // ---------- theme ----------
  const root = document.documentElement;
  try {
    const saved = localStorage.getItem("theme");
    if (saved) root.dataset.theme = saved;
  } catch (_) { /* storage unavailable */ }
  $("#themeToggle").addEventListener("click", () => {
    const dark = root.dataset.theme
      ? root.dataset.theme === "dark"
      : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    try { localStorage.setItem("theme", root.dataset.theme); } catch (_) { /* ignore */ }
  });

  // ---------- helpers ----------
  $("#today").textContent = new Intl.DateTimeFormat("ko-KR", {
    year: "numeric", month: "long", day: "numeric", weekday: "long",
  }).format(new Date());

  function toDate(value) {
    // 샘플 데이터는 "-3h"처럼 현재 시각 기준 상대값을 씁니다.
    const rel = /^-(\d+)h$/.exec(value);
    return rel ? new Date(Date.now() - rel[1] * 3600e3) : new Date(value);
  }

  function ago(date) {
    const min = Math.round((Date.now() - date) / 60000);
    if (min < 1) return "방금 전";
    if (min < 60) return `${min}분 전`;
    const h = Math.round(min / 60);
    if (h < 24) return `${h}시간 전`;
    const d = Math.round(h / 24);
    if (d < 7) return `${d}일 전`;
    return date.toLocaleDateString("ko-KR", { month: "long", day: "numeric" });
  }

  const label = (key) => state.data.categories[key] || "기타";
  const catVar = (key) => `--cat: var(--c-${key in state.data.categories ? key : "industry"})`;

  function linkAttrs(item) {
    return item.link && item.link !== "#"
      ? `href="${esc(item.link)}" target="_blank" rel="noopener noreferrer"`
      : `href="#" aria-disabled="true" onclick="return false"`;
  }

  function byline(item) {
    return `<div class="byline"><span>${esc(item.source)}</span><span><time datetime="${item.date.toISOString()}">${ago(item.date)}</time></span></div>`;
  }

  function listItem(item, withTag = false) {
    return `<li><a ${linkAttrs(item)}>
      ${withTag ? `<span class="tag" style="${catVar(item.category)}">${esc(label(item.category))}</span>` : ""}
      <h3 class="headline">${esc(item.title)}</h3>${byline(item)}</a></li>`;
  }

  // ---------- rendering ----------
  function renderNav() {
    const cats = [["all", "전체"], ...Object.entries(state.data.categories)];
    $("#catnav").innerHTML = cats.map(([key, name]) =>
      `<button type="button" data-cat="${key}" aria-pressed="${state.category === key}">${esc(name)}</button>`
    ).join("");
  }

  function renderFront(items) {
    const [lead, ...rest] = items;
    const secondary = rest.slice(0, 4);
    const related = rest.slice(4).filter((i) => i.category === lead.category).slice(0, 3);
    const shown = new Set([lead, ...secondary, ...related].map((i) => i.id));

    const sections = Object.keys(state.data.categories).map((key) => {
      const list = items.filter((i) => i.category === key && !shown.has(i.id)).slice(0, 4);
      if (!list.length) return "";
      return `<section style="${catVar(key)}">
        <div class="section-head"><h2>${esc(label(key))}</h2>
          <button class="more" type="button" data-cat="${key}">더보기 →</button></div>
        <ul class="list">${list.map((i) => listItem(i)).join("")}</ul>
      </section>`;
    }).join("");

    return `
      <div class="front">
        <div class="lead" style="${catVar(lead.category)}">
          <a ${linkAttrs(lead)}>
            <span class="tag">${esc(label(lead.category))} · 톱기사</span>
            <h2 class="headline">${esc(lead.title)}</h2>
            ${byline(lead)}
          </a>
          ${related.length ? `<div class="related"><h3>${esc(label(lead.category))} 관련 기사</h3>
            <ul>${related.map((i) => `<li><a ${linkAttrs(i)}><span class="headline">${esc(i.title)}</span></a></li>`).join("")}</ul>
          </div>` : ""}
        </div>
        <div class="secondary">
          ${secondary.map((i) => `<a ${linkAttrs(i)} style="${catVar(i.category)}">
            <span class="tag">${esc(label(i.category))}</span>
            <h3 class="headline">${esc(i.title)}</h3>${byline(i)}</a>`).join("")}
        </div>
      </div>
      <div class="sections">${sections}</div>`;
  }

  function renderResults(items) {
    const title = state.query
      ? `‘${esc(state.query)}’ 검색 결과`
      : esc(label(state.category));
    const body = items.length
      ? `<ul class="list">${items.map((i) => listItem(i, true)).join("")}</ul>`
      : `<p class="empty">해당하는 토목 기사가 없습니다.</p>`;
    return `<div class="results">
      <div class="results-head"><h2>${title}</h2><span class="meta">${items.length}건</span></div>
      ${body}</div>`;
  }

  function renderSidebar(all) {
    const counts = Object.keys(state.data.categories).map((key) => [key, all.filter((i) => i.category === key).length]);
    const max = Math.max(1, ...counts.map(([, n]) => n));
    $("#stats").innerHTML = counts.map(([key, n]) => `<li><button type="button" data-cat="${key}" style="${catVar(key)}">
      <span>${esc(label(key))}</span><span class="bar"><i style="width:${(n / max) * 100}%"></i></span><span class="n">${n}</span>
    </button></li>`).join("");
    $("#latest").innerHTML = all.slice(0, 7).map((i) => `<li><a ${linkAttrs(i)}>${esc(i.title)}</a></li>`).join("");
  }

  function render() {
    const all = state.data.items;
    const q = state.query.trim().toLowerCase();
    let items = all;
    if (state.category !== "all") items = items.filter((i) => i.category === state.category);
    if (q) items = items.filter((i) => i.title.toLowerCase().includes(q) || i.source.toLowerCase().includes(q));

    renderNav();
    $("#content").innerHTML = state.category === "all" && !q && items.length
      ? renderFront(items)
      : renderResults(items);
  }

  function setCategory(cat) {
    state.category = cat;
    render();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  document.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-cat]");
    if (btn) setCategory(btn.dataset.cat);
  });
  let timer;
  $("#search").addEventListener("input", (e) => {
    clearTimeout(timer);
    timer = setTimeout(() => { state.query = e.target.value; render(); }, 150);
  });

  // ---------- data ----------
  async function load(url) {
    const res = await fetch(url, { cache: "no-cache" });
    if (!res.ok) throw new Error(res.status);
    const data = await res.json();
    if (!data.items || !data.items.length) throw new Error("empty");
    return data;
  }

  async function init() {
    $("#content").innerHTML = Array.from({ length: 8 }, () => '<div class="skeleton"></div>').join("");
    let data;
    try {
      data = await load("data/news.json");
    } catch (_) {
      try {
        data = await load("data/sample.json");
      } catch (err) {
        $("#content").innerHTML = '<p class="empty">기사를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.</p>';
        return;
      }
    }
    data.items.forEach((i) => { i.date = toDate(i.published); });
    data.items.sort((a, b) => b.date - a.date);
    state.data = data;

    if (data.sample) {
      const notice = $("#notice");
      notice.hidden = false;
      notice.textContent = "지금 보이는 기사는 화면 구성을 보여주기 위한 예시입니다. 자동 수집(GitHub Actions)이 처음 실행되면 실제 토목 기사로 바뀝니다.";
    } else if (data.updated) {
      $("#updated").textContent = `마지막 업데이트 ${ago(new Date(data.updated))}`;
    }

    renderSidebar(data.items);
    render();
  }

  init();
})();
