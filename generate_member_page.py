#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
メンバーページ生成スクリプト
members.jsonからHTMLページを生成します
"""

import json
import os
from datetime import datetime

def load_members_data(json_file='members.json'):
    """JSONファイルからメンバーデータを読み込み"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"エラー: {json_file} が見つかりません")
        return None
    except json.JSONDecodeError:
        print(f"エラー: {json_file} のJSON形式が正しくありません")
        return None

def generate_teacher_html(teacher):
    """教員のHTMLを生成"""
    links_html = ""
    if 'links' in teacher:
        for link in teacher['links']:
            links_html += f'<a href="{link["url"]}">{link["type"]}</a>\n'
    
    return f'''
                    <div class="member">
                        <img src="{teacher['image']}" alt="メンバー画像">
                        <div class="member_content">
                            <h1>{teacher['name']}</h1>
                            <p>{teacher['position']}</p>
                            {links_html}
                        </div>
                    </div>'''

def generate_student_html(student):
    """学生のHTMLを生成（写真なし、一言コメント付き）"""
    comment = student.get('comment', '')
    return f'''
                    <div class="student_item">
                        <div class="student_content">
                            <h3>{student['name']}</h3>
                            <p class="comment">{comment}</p>
                        </div>
                    </div>'''

def generate_member_page(data, output_file='Member.html'):
    """メンバーページのHTMLを生成"""
    
    # ヘッダー部分
    header = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>先端モビリティ工学研究室</title>
    <meta name="description" content="先端モビリティ工学研究室のホームページ">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/style2_sigesawa.css?v=20250831">
    <link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css">
    <link rel="icon" href="img/logotxt.svg" type="image/x-icon">
    <script src="javascript/script_sigesawa.js?v=20250831"></script>
    <style>
        .student_item {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .student_content h3 {
            margin: 0 0 5px 0;
            color: #333;
            font-size: 1.2em;
        }
        .grade {
            margin: 0 0 10px 0;
            color: #666;
            font-weight: bold;
            font-size: 0.9em;
        }
        .comment {
            margin: 0;
            color: #555;
            font-size: 0.9em;
            line-height: 1.4;
        }
        .student_wrapper {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .grade_section {
            margin: 30px 0;
        }
        .grade_section h3 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="bg_1">
        <div class="header">
            <div class="logo">
                <a href="index.html">
                    <img src="img/logo.svg" alt="研究室の写真">
                </a>
            </div>
            <div class="nav">
                <ul class="menu clearfix">
                    <li class="parent">
                        <a href="index.html">Home</a>
                        <ul class="children">
                        </ul>
                    </li>
                    <li class="parent">
                        <a href="Member.html">Member</a>
                        <ul class="children">
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container">'''

    # 教員セクション
    teachers_html = '''
        <div id="member" class="container_member">
            <h3>Member</h3>
            
            <div class="teachers">
                <h2>教員</h2>
                <div class="teacher_wrapper">'''
    
    for teacher in data['members']['teachers']:
        teachers_html += generate_teacher_html(teacher)
    
    teachers_html += '''
                </div>
            </div>'''

    # 学生セクション
    students_html = '''
            <div class="students">
                <h2>学生</h2>'''
    
    # 博士課程
    if data['members']['students']['doctoral']:
        students_html += '''
                <div class="grade_section">
                    <h3>博士課程</h3>
                    <div class="student_wrapper">'''
        for student in data['members']['students']['doctoral']:
            students_html += generate_student_html(student)
        students_html += '''
                    </div>
                </div>'''
    
    # 修士課程 M2
    if data['members']['students']['master']['M2']:
        students_html += '''
                <div class="grade_section">
                    <h3>修士課程 2年</h3>
                    <div class="student_wrapper">'''
        for student in data['members']['students']['master']['M2']:
            students_html += generate_student_html(student)
        students_html += '''
                    </div>
                </div>'''
    
    # 修士課程 M1
    if data['members']['students']['master']['M1']:
        students_html += '''
                <div class="grade_section">
                    <h3>修士課程 1年</h3>
                    <div class="student_wrapper">'''
        for student in data['members']['students']['master']['M1']:
            students_html += generate_student_html(student)
        students_html += '''
                    </div>
                </div>'''
    
    # 学部生
    if data['members']['students']['bachelor']:
        students_html += '''
                <div class="grade_section">
                    <h3>学部生 4年</h3>
                    <div class="student_wrapper">'''
        for student in data['members']['students']['bachelor']:
            students_html += generate_student_html(student)
        students_html += '''
                    </div>
                </div>'''
    
    students_html += '''
            </div>
        </div>
    </div>'''

    # フッター
    footer = '''
<footer>
    <div class="logo_address">
        <div class="logo_footer">
            <img src="img/logo_white.svg" alt="ロゴ">
        </div>
        <div class="address">
            <p></p>
                <p>Copyright © Laboratory of Advanced Mobility and Transportation Engineering. All Rights Reserved.</p>
            <p></p>
        </div>
    </div>
    <div class="copyright">
        <p></p>
    </div>
</footer> 

    <script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
    <script>
        // Swiperの初期化
        var swiper = new Swiper('.swiper', {
            slidesPerView: 1,
            spaceBetween: 10,
            
            breakpoints: {
                600: {
                    slidesPerView: 4,
                    spaceBetween: 20,
                }
            },
            pagination: {
                el: '.swiper-pagination',
                type: 'bullets',
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            loop: true,
            autoplay: {
                delay: 5000,
            },
        });
    </script>
    <style>
        .swiper-pagination-bullet {
        /*ドットの色を変更*/
            background-color: #000 ; 
        }
        .swiper-button-prev {
            top: 10px;
            left: 1000px; /* 左の矢印を左に配置 */
            color: #000; /* 色を赤に変更 */
        }

        .swiper-button-next {
            top: 10px;
            right: 100px; /* 右の矢印を右に配置 */
            color: #000; /* 色を青に変更 */
        }

        .swiper-button-next::after{
            content: '→';/* ボタンの矢印変更 */
            color: #000;
            font-size: 2rem;
        }
        .swiper-button-prev::after{
            content: '←';/* ボタンの矢印変更 */
            color: #000;
            font-size: 2rem;
        }
    </style>

</body>

</html>'''

    # 生成日時のコメントを追加
    generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment = f'<!-- Generated from members.json on {generated_time} -->\n'
    
    # 完全なHTMLを組み立て
    full_html = comment + header + teachers_html + students_html + footer
    
    # ファイルに書き込み
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"✅ メンバーページが生成されました: {output_file}")
        print(f"📊 教員: {data['summary']['total_teachers']}名")
        print(f"�� 学生: {data['summary']['total_students']}名")
        return True
    except Exception as e:
        print(f"❌ エラー: ファイルの書き込みに失敗しました - {e}")
        return False

def main():
    """メイン関数"""
    print("🚀 メンバーページ生成スクリプトを開始します...")
    
    # JSONデータを読み込み
    data = load_members_data()
    if not data:
        return
    
    # メンバーページを生成
    success = generate_member_page(data)
    
    if success:
        print("🎉 メンバーページの生成が完了しました！")
    else:
        print("💥 メンバーページの生成に失敗しました。")

if __name__ == "__main__":
    main()
