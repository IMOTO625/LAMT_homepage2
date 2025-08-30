document.addEventListener('DOMContentLoaded', function () {
    fetch('blog_data.json') // JSONデータを取得
        .then(response => response.json())
        .then(data => {
            const blogSection = document.querySelector('.blog section');
            blogSection.innerHTML = ''; // 既存の内容をクリア

            data.forEach(post => {
                const article = document.createElement('article');
                article.innerHTML = `
                    <img class="blog-image" src="${post.image || 'img/default.jpg'}" alt="記事画像">
                    <div class="blog_text">
                        <h2>${post.title}</h2>
                        <p class="preview">${post.content.slice(0, 150)}...</p>
                        <p class="full-content" style="display: none;">${post.content}</p>
                        <button class="read-more">続きを読む</button>
                        <button class="close" style="display: none;">折りたたむ</button>
                        <div class="info">
                            <p><small>投稿者: ${post.author}</small></p>
                            <p><small>投稿日時: ${new Date(post.timestamp).toLocaleString()}</small></p>
                        </div>
                    </div>
                `;
                blogSection.appendChild(article);
            });

            // 記事の表示切り替えイベントを設定
            addReadMoreEventListeners();
        })
        .catch(error => console.error('ブログデータの取得に失敗しました:', error));
});

function addReadMoreEventListeners() {
    document.querySelectorAll('.read-more').forEach(button => {
        button.addEventListener('click', function () {
            const article = button.closest('article');
            article.querySelector('.full-content').style.display = 'block';
            article.querySelector('.preview').style.display = 'none';
            article.querySelector('.close').style.display = 'block';
            button.style.display = 'none';
        });
    });

    document.querySelectorAll('.close').forEach(button => {
        button.addEventListener('click', function () {
            const article = button.closest('article');
            article.querySelector('.full-content').style.display = 'none';
            article.querySelector('.preview').style.display = 'block';
            article.querySelector('.read-more').style.display = 'block';
            button.style.display = 'none';
        });
    });
}

const images = ['img/lab.jpg', 'img/member.jpg', 'img/baseball.jpg', 'img/semiroom.jpg', 'img/bbq.jpg']
let current = 0

function changeImage() {
    const imgElement = document.getElementById('slideshow-image')
    current = (current + 1) % images.length
    imgElement.src = images[current]
}

setInterval(changeImage, 5000) // xxxxmsごとに画像を切り替える



document.addEventListener('DOMContentLoaded', function () {
    fetch('blog_data.json') // JSONデータを取得
        .then(response => response.json())
        .then(data => {
            const blogHomeSection = document.querySelector('.blog_home section');
            blogHomeSection.innerHTML = ''; // 既存の内容をクリア

            // 最新の4件のブログ記事を取得
            data.slice(0, 4).forEach(post => {
                const article = document.createElement('article');
                article.innerHTML = `
                    <img class="blog-image_home" src="${post.image || 'img/default.jpg'}" alt="記事画像">
                    <div class="blog_text_home">
                        <h2>${post.title}</h2>
                        <p>by: ${post.author}</p>
                    </div>
                `;
                blogHomeSection.appendChild(article);
            });
        })
        .catch(error => console.error('ブログデータの取得に失敗しました:', error));
});

