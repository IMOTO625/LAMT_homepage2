#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ブログHTML生成スクリプト
blog_data.jsonのデータを読み込んで、blog2.htmlのようなHTMLファイルを生成する
"""

import json
import os
from datetime import datetime
from jinja2 import Template

def load_blog_data(json_file):
    """JSONファイルからブログデータを読み込む"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ {len(data)}件の記事を読み込みました")
        return data
    except FileNotFoundError:
        print(f"❌ エラー: {json_file} が見つかりません")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ エラー: JSONの形式が正しくありません - {e}")
        return None

def format_timestamp(timestamp_str):
    """タイムスタンプを日本語形式に変換"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return timestamp_str

def process_blog_data(data):
    """ブログデータを処理してHTML生成用に準備"""
    # タイムスタンプでソート（新しい順）
    sorted_data = sorted(data, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # タイムスタンプをフォーマット
    for item in sorted_data:
        item['formatted_timestamp'] = format_timestamp(item.get('timestamp', ''))
        # プレビューテキスト（最初の150文字）
        content = item.get('content', '')
        item['preview'] = content[:150] + '...' if len(content) > 150 else content
    
    return sorted_data

def get_years_from_data(data):
    """データから年を抽出してリストを作成"""
    years = set()
    for item in data:
        timestamp = item.get('timestamp', '')
        if timestamp:
            try:
                year = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).year
                years.add(year)
            except:
                pass
    return sorted(list(years), reverse=True)

def create_html_template():
    """HTMLテンプレートを作成"""
    return """<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>先端モビリティ工学研究室</title> <!--サイトのタイトル-->
    <meta name="discription" content="先端モビリティ工学研究室のホームページ"> <!--サイトの説明文-->
    <link rel="stylesheet" href="css/reset.css"> <!--reset cssはブラウザごとに異なるデフォルトのCSSをリセットし、統一する。最初に読み込む-->
    <link rel="stylesheet" href="css/style2_sigesawa.css"> <!--cssファイルの読み込み-->
    <link rel="icon" href="img/logotxt.svg" type="image/x-icon"> <!--タブアイコン（ファビコン）の設定-->
</head>

<body>
    <div class="bg_1">
        <div class="header"> <!--デザインを俯瞰してどうdiv分割するかを考えるとよい-->
            <div class="logo"> <!--ロゴクラスを作ることで、ロゴクラスに対してcssを適用できる-->
                <a href="index.html">
                    <img src="img/logo.svg" alt="研究室の写真"> <!--画像-->
                </a>
            </div>
            <div class="nav"> <!--ナビゲーション-->
                <ul class="menu clearfix">
                    <li class="parent">
                        <a href="index.html">ホーム</a>
                        <ul class="children">
                            <li><a href="#about">当研究室について</a></li>
                            <li><a href="#blog_small">新着のブログ</a></li>
                            <li><a href="#calen">今後の予定</a></li>
                        </ul>
                    </li>
                    <li class="parent">
                        <a href="introduction.html">研究室紹介</a>
                        <ul class="children">
                            <li><a href="#setubi">設備紹介</a></li>
                            <li><a href="#member">メンバー紹介</a></li>
                            <li><a href="#gazou">ギャラリー</a></li>
                        </ul>
                    </li>
                    <li class="parent">
                        <a href="research.html">研究紹介</a>
                        <ul class="children">
                            <li><a href="#gyouseki">研究業績</a></li>
                            <li><a href="#shoukai">研究紹介</a></li>

                        </ul>
                    </li>
                    <li class="parent">
                        <a href="blog.html">ブログ</a>
                    </li>
                    <li class="parent">
                        <a href="sotomuke.html">連絡先・配属前の学生へ</a>
                        <ul class="children">
                            <li><a href="#先生から一言">教員より</a></li>
                            <li><a href="#学生から一言">学生より</a></li>
                            <li><a href="#住所・連絡先">コンタクト</a></li>
                            <li><a href="#進路">進路情報</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div class="bg_2">
        <div class="blog">
            <section>
            {% for article in articles %}
                <article>
                    <img class="blog-image" src="{{ article.image }}" alt="記事画像">
                    <div class="blog_text">
                        <h2>{{ article.title }}</h2>
                        <p class="preview">{{ article.preview }}</p> <!-- 最初の150文字を表示 -->
                        <p class="full-content" style="display: none;">{{ article.content }}</p> <!-- 完全な記事内容 -->
                        <button class="read-more">続きを読む</button>
                        <button class="close" style="display: none;">折りたたむ</button>
                        <div class="info">
                            <p><small>投稿者:{{ article.author }}</small></p>
                            <p><small>投稿日時:{{ article.formatted_timestamp }}</small></p>
                        </div>
                    </div>
                </article>
            {% endfor %}
            </section>
            <div class="organize">
                <h1>年別ブログ</h1>
                <ol>
                    {% for year in years %}
                    <li><a>{{ year }}</a></li>
                    {% endfor %}
                </ol>
            </div>
        </div>
    </div>
    
    <script>
        // 続きを読むボタンの機能
        document.addEventListener('DOMContentLoaded', function() {
            const readMoreButtons = document.querySelectorAll('.read-more');
            const closeButtons = document.querySelectorAll('.close');
            
            readMoreButtons.forEach((button, index) => {
                button.addEventListener('click', function() {
                    const preview = this.parentElement.querySelector('.preview');
                    const fullContent = this.parentElement.querySelector('.full-content');
                    const closeBtn = this.parentElement.querySelector('.close');
                    
                    preview.style.display = 'none';
                    fullContent.style.display = 'block';
                    this.style.display = 'none';
                    closeBtn.style.display = 'inline-block';
                });
            });
            
            closeButtons.forEach((button, index) => {
                button.addEventListener('click', function() {
                    const preview = this.parentElement.querySelector('.preview');
                    const fullContent = this.parentElement.querySelector('.full-content');
                    const readMoreBtn = this.parentElement.querySelector('.read-more');
                    
                    preview.style.display = 'block';
                    fullContent.style.display = 'none';
                    this.style.display = 'none';
                    readMoreBtn.style.display = 'inline-block';
                });
            });
        });
    </script>
</body>
<footer>
    <div class="logo_address">
        <div class="logo_footer">
            <img src="img/logo_white.svg" alt="ロゴ">
        </div>
        <div class="address">
            <p>〒060-0810　札幌市北区北１０条西８丁目</p>
            <p>北海道大学大学院　理学研究院化学部門 　理学部7号館304号室</p>
            <p>Tell：011-706-4665</p>
        </div>
    </div>
    <div class="copyright">
        <p>Copyright @Laboratry of Advanced Mobility and Transportation Engineering. All Rights Reserved</p>
    </div>
</footer>

</html>"""

def generate_html(data, output_file):
    """HTMLファイルを生成"""
    try:
        # データを処理
        processed_data = process_blog_data(data)
        years = get_years_from_data(data)
        
        # テンプレートを作成
        template = Template(create_html_template())
        
        # HTMLを生成
        html_content = template.render(articles=processed_data, years=years)
        
        # ファイルに書き込み
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ HTMLファイルを生成しました: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ エラー: HTML生成中にエラーが発生しました - {e}")
        return False

def main():
    """メイン処理"""
    print("=== ブログHTML生成スクリプト ===")
    
    # ファイルパス
    json_file = "blog_data.json"
    output_file = "blog.html"
    
    # JSONデータを読み込み
    data = load_blog_data(json_file)
    if data is None:
        return
    
    # HTMLファイルを生成
    if generate_html(data, output_file):
        print(f"\n=== 処理完了 ===")
        print(f"生成されたファイル: {output_file}")
        print(f"処理された記事数: {len(data)}件")
        
        # 記事一覧を表示
        print("\n=== 処理された記事 ===")
        for i, article in enumerate(process_blog_data(data), 1):
            print(f"{i}. {article['title']} (投稿者: {article['author']}, {article['formatted_timestamp']})")
    else:
        print("❌ HTML生成に失敗しました")

if __name__ == "__main__":
    main()
