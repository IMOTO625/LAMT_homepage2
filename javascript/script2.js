document.addEventListener("DOMContentLoaded", () => {
    fetch("data/researchData.json")
        .then(response => {
            if (!response.ok) {
                throw new Error("JSONデータの取得に失敗しました");
            }
            return response.json();
        })
        .then(researchData => {
            renderResearch(researchData);

            document.querySelectorAll(".filter-btn").forEach(btn => {
                btn.addEventListener("click", () => {
                    // ボタンのアクティブ状態を管理
                    document.querySelectorAll(".filter-btn").forEach(button => {
                        button.classList.remove("active");  // すべてのボタンからactiveを外す
                    });
                    btn.classList.add("active");  // クリックされたボタンにactiveを追加

                    const year = btn.dataset.year ? parseInt(btn.dataset.year) : null;
                    const category = btn.dataset.category || null;

                    if (btn.classList.contains('show-all')) {
                        renderResearch(researchData); // すべてのデータを表示
                    } else {
                        const filteredData = researchData.filter(item => {
                            const yearMatch = year === null || item.year === year;
                            const categoryMatch = category === null || item.category === category;
                            return yearMatch && categoryMatch;
                        });
                        renderResearch(filteredData); // フィルタリングされたデータを表示
                    }
                });
            });
        })
        .catch(error => {
            console.error("エラー:", error);
        });
});

// 研究テーマの一覧を作成
function renderResearch(data) {
    const container = document.getElementById("research-container");
    container.innerHTML = "";
    data.forEach(item => {
        const researchHTML = `
            <div class="research-item">
                <h1 class="research-title">${item.title}</h1>
                <div class="research-details">
                    <img src="${item.image}" alt="${item.title}の画像" class="research-image">  <!-- 画像を追加 -->
                    <p>${item.details}</p>
                </div>
            </div>`;
        container.insertAdjacentHTML("beforeend", researchHTML);
    });

    // クリックで詳細を開閉
    document.querySelectorAll(".research-title").forEach(title => {
        title.addEventListener("click", () => {
            const details = title.nextElementSibling;
            details.classList.toggle("active");
        });
    });
}
