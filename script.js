// サンプル研究データの読み込み
import researchData from './researchData.json';

// 研究詳細の描画関数
function renderResearch(data) {
    const container = document.getElementById("research-container");
    container.innerHTML = ""; // 一旦クリア
    data.forEach(item => {
        const researchHTML = `
            <div class="research-item" id="${item.id}">
                <h1>${item.title}</h1>
                <p>${item.details}</p>
            </div>`;
        container.insertAdjacentHTML("beforeend", researchHTML);
    });
}

// 研究テーマ一覧の描画関数
function renderThemes(data) {
    const container = document.getElementById("research-themes");
    container.innerHTML = ""; // 一旦クリア
    data.forEach(item => {
        const themeHTML = `
            <dl><dd><a href="#${item.id}">${item.title}</a></dd></dl>`;
        container.insertAdjacentHTML("beforeend", themeHTML);
    });
}

// 初期表示
renderResearch(researchData);
renderThemes(researchData);

// フィルターボタンのイベントリスナー
document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const year = btn.dataset.year;
        const category = btn.dataset.category;

        const filteredData = researchData.filter(item => {
            return (!year || item.year == year) && (!category || item.category === category);
        });

        renderResearch(filteredData);
        renderThemes(filteredData);
    });
});

// スムーズスクロール設定
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault();
        const targetId = this.getAttribute("href").substring(1);
        const targetElement = document.getElementById(targetId);
        targetElement.scrollIntoView({ behavior: "smooth", block: "start" });
    });
});
