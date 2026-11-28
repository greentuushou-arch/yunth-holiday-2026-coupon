"""wide.html(横長レイアウトの元データ)から「両脇レール」版を作り、
公開ページ index.html と rail.html(同じ内容)に書き出す。

- 1180px 以上: 中央に 640px のスマホ幅カラム + 左レール(メニュー) + 右レール(2つのクーポン)
- 1180px 未満: wide.html と同じ見え方(スマホは下部バー + メニューボタン)

中央カラムの中はコンテナクエリで切り替えるので、PC でもスマホと同じレイアウトになる。
中身の修正は wide.html に入れて `python tools/build_rail.py` で作り直す(index.html は直接直さない)。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "wide.html").read_text(encoding="utf-8")

css_start = src.index("<style>") + len("<style>")
css_end = src.index("</style>")
css = src[css_start:css_end]

# 1) ビューポート基準のメディアクエリを、中央カラム(main)基準のコンテナクエリへ
css = css.replace("@media (min-width:768px) and (max-aspect-ratio:3/2){.fv-photo img{object-position:45% 50%}}\n", "")
css = re.sub(r"@media ((?:\((?:min|max)-width:\d+px\)(?: and )?)+)\{", r"@container main \1{", css)

# 2) vw をカラム幅基準の cqw へ(スマホでは main = 画面幅なので同じ値)
css = re.sub(r"(\d)vw\b", r"\1cqw", css)

# 3) 下部バーは main の外にあるので、ビューポート基準のまま残す
mbar_rules = "\n".join(line for line in css.splitlines() if line.strip().startswith(".mbar"))
mbar_rules = re.sub(r"(\d)cqw\b", r"\1vw", mbar_rules)

RAIL_CSS = """
/* ===== 両脇レールのフレーム ===== */
:root{--col:640px;--rail:268px}
.main{container:main / inline-size;background:var(--cream)}
@media (max-width:767px){
""" + mbar_rules + """
}
.rail{position:fixed;top:0;bottom:0;width:var(--rail);z-index:30;display:none;flex-direction:column;justify-content:center;padding:28px 22px;color:#fff}
.rail--l{left:max(16px,calc(50% - var(--col)/2 - var(--rail) - 36px))}
.rail--r{right:max(16px,calc(50% - var(--col)/2 - var(--rail) - 36px));gap:14px}
.rail .logo{width:128px}
.rail-sub{margin-top:12px;font-family:var(--num);font-weight:500;font-size:14px;letter-spacing:.2em;white-space:nowrap;color:var(--gold-l)}
.rail-ttl{margin-top:10px;font-family:var(--en);font-style:italic;font-weight:700;font-size:40px;line-height:.95;background:var(--gold-grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.menu{list-style:none;margin-top:26px}
.menu a{display:flex;gap:12px;align-items:baseline;padding:11px 2px;color:#fff;text-decoration:none;font-weight:700;font-size:16px;letter-spacing:.06em;border-bottom:1px solid #ffffff33;white-space:nowrap;transition:color .2s}
.menu a b{font-family:var(--num);font-weight:600;font-size:15px;color:var(--gold-l);width:1.7em}
.menu a:hover,.menu a.is-cur{color:var(--gold-l)}
.rcpn{position:relative;background:#fffdf9;color:var(--ink);text-align:center;padding:18px 14px 14px;outline:1px solid var(--gold);outline-offset:-6px}
.rcpn-for{font-weight:700;font-size:15px;letter-spacing:.04em;line-height:1.4}
.rcpn-for b{display:block;font-size:17px;color:var(--red-d)}
.rcpn .first{display:flex;width:fit-content;margin:8px auto 0;font-size:14px;padding:.2em .6em}
.rcpn .first b{font-size:1.5em}
.rcpn-two{margin-top:6px;font-weight:700;font-size:16px}
.rcpn-two b{font-family:var(--num);font-weight:600;font-size:1.5em;color:var(--red)}
.rcpn .off{font-size:56px;color:var(--red)}
.rcpn-cpn{font-weight:900;font-size:20px;color:var(--red);line-height:1.3}
.rcpn .note{margin-top:2px;font-size:14px;line-height:1.5}
.rcpn-tm{margin-top:6px;padding-top:6px;border-top:1px solid #eadfd3;font-family:var(--num);font-weight:600;font-size:15px;line-height:1.5}
.rcpn-tm small{font-family:var(--sans);font-size:14px}
.rcpn .btn{width:100%;margin-top:10px;padding:11px 8px;font-size:16px;letter-spacing:.04em}
@media (max-height:860px){.rail--r{gap:10px;padding-block:14px}.rcpn{padding:12px 12px 10px}.rcpn-for{font-size:14px}.rcpn-for b{font-size:15px}.rcpn .first{margin-top:4px}.rcpn-two{margin-top:2px}.rcpn .off{font-size:44px}.rcpn-cpn{font-size:17px}.rcpn-tm{font-size:14px}.rcpn .btn{margin-top:6px;padding:8px}}
.menubtn{position:fixed;top:12px;right:12px;z-index:40;width:56px;height:56px;padding:0;border-radius:50%;border:1px solid var(--gold);background:#9e0f22;color:var(--gold-l);font-weight:700;font-size:13px;line-height:1;letter-spacing:0;cursor:pointer;box-shadow:0 2px 10px #0005}
.menubtn span{display:block;width:22px;height:2px;margin:0 auto 5px;background:var(--gold-l);box-shadow:0 -6px 0 var(--gold-l)}
.drawer{position:fixed;inset:0;z-index:35;background:#9e0f22f5;color:#fff;padding:92px 32px 32px;overflow:auto;opacity:0;visibility:hidden;transition:opacity .3s,visibility .3s}
.drawer.is-open{opacity:1;visibility:visible}
.drawer .menu a{font-size:18px;padding:15px 4px}
@media (min-width:1180px){
  body{background:radial-gradient(120% 90% at 50% 0%,#e9213a 0%,#c3142b 55%,#9e0f22 100%) fixed}
  .main{max-width:var(--col);margin:0 auto;box-shadow:0 0 70px #0000004d}
  .rail{display:flex}
  .menubtn,.drawer{display:none}
}
"""
css = css + RAIL_CSS

MENU = """<ul class="menu" data-menu>
    <li><a href="#offer-gift"><b>01</b>2点そろえてクーポン</a></li>
    <li><a href="#calendar"><b>02</b>クーポンの期間</a></li>
    <li><a href="#gift"><b>03</b>スペシャルギフトBOX</a></li>
    <li><a href="#post"><b>04</b>ポスト投函BOX</a></li>
    <li><a href="#terms"><b>05</b>クーポンのご注意</a></li>
  </ul>"""

RAILS = f"""
<aside class="rail rail--l" aria-label="ページメニュー">
  <span class="logo" role="img" aria-label="Yunth"></span>
  <p class="rail-ttl">Holiday<br>Collection</p>
  {MENU}
</aside>

<aside class="rail rail--r" aria-label="クーポン">
  <div class="rcpn" data-live="gift-cpn">
    <p class="rcpn-for">大切な人へ<b>スペシャルギフトBOX</b></p>
    <span class="first"><span>先着</span><b>1,000</b><span>名様</span></span>
    <p class="rcpn-two"><b>2</b>点で</p>
    <span class="off"><b>1,000</b><span class="off__u"><i class="y">円</i><i class="o">OFF</i></span></span>
    <p class="rcpn-cpn">クーポン<sup>※7</sup></p>
    <p class="note">※7 【公式】Yunth Store <span class="nw">楽天市場店で使用可能。</span></p>
    <p class="rcpn-tm">12/1<small>(火)</small> 0:00<br>〜 12/28<small>(月)</small> 23:59</p>
    <a class="btn btn-red" data-coupon="gift" href="#offer-gift">クーポン獲得</a>
  </div>
  <div class="rcpn" data-live="post-cpn">
    <p class="rcpn-for">自分へ<b>ポスト投函BOX</b></p>
    <p class="rcpn-two"><b>2</b>点で</p>
    <span class="off"><b>500</b><span class="off__u"><i class="y">円</i><i class="o">OFF</i></span></span>
    <p class="rcpn-cpn">クーポン<sup>※7</sup></p>
    <p class="note">※7 【公式】Yunth Store <span class="nw">楽天市場店で使用可能。</span></p>
    <p class="rcpn-tm">12/1<small>(火)</small> 0:00<br>〜 12/11<small>(金)</small> 9:59</p>
    <a class="btn btn-red" data-coupon="post" href="#offer-post">クーポン獲得</a>
  </div>
</aside>

<button class="menubtn" type="button" aria-label="メニューを開く" aria-expanded="false" data-menubtn><span></span>メニュー</button>
<nav class="drawer" aria-label="ページメニュー" data-drawer>
  {MENU}
</nav>

<main class="main">
"""

DRAWER_JS = """
/* ---- メニュー(スマホのドロワー/PCの現在地) ---- */
(() => {
  const btn = document.querySelector("[data-menubtn]"), drawer = document.querySelector("[data-drawer]");
  const setOpen = open => { drawer.classList.toggle("is-open", open); btn.setAttribute("aria-expanded", open); btn.lastChild.textContent = open ? "閉じる" : "メニュー"; };
  btn.addEventListener("click", () => setOpen(!drawer.classList.contains("is-open")));
  drawer.addEventListener("click", e => { if (e.target.closest("a")) setOpen(false); });
  const links = [...document.querySelectorAll(".rail .menu a")];
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    links.forEach(a => a.classList.toggle("is-cur", a.getAttribute("href") === "#" + e.target.id));
  }), { rootMargin: "-45% 0px -50% 0px" });
  ["offer-gift", "calendar", "gift", "post", "terms"].forEach(id => { const el = document.getElementById(id); if (el) io.observe(el); });
})();
</script>"""

out = src[:css_start] + css + src[css_end:]
out = out.replace("<body>\n", "<body>\n" + RAILS, 1)
mbar_at = out.index('<nav class="mbar"')
out = out[:mbar_at] + "</main>\n\n" + out[mbar_at:]
last_script_end = out.rindex("</script>")
out = out[:last_script_end] + DRAWER_JS + out[last_script_end + len("</script>"):]
assert out.count("<main") == 1 and out.count("</main>") == 1

for name in ("index.html", "rail.html"):
    (ROOT / name).write_text(out, encoding="utf-8", newline="\n")
print("index.html / rail.html written:", len(out), "chars")
