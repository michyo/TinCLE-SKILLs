import os
import re

def generate_index_html():
    base_dir = "."
    # 'version'から始まるディレクトリを探してソート（新しい順にしたい場合は reverse=True）
    versions = sorted([d for d in os.listdir(base_dir) if os.path.isdir(d) and d.startswith("version")], reverse=True)

    html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TinCLE Talent Chips (SKILL.md) Archive</title>
    <style>
        :root {
            --bg-color: #121214;
            --text-color: #e0e0e0;
            --accent-color: #ff007f;
            --card-bg: #1e1e24;
            --hover-color: #ff4da6;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            text-align: center;
            color: var(--accent-color);
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(255, 0, 127, 0.5);
        }
        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 40px;
            font-style: italic;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .version-section {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            border-left: 5px solid var(--accent-color);
        }
        .version-title {
            font-size: 1.8rem;
            color: #fff;
            margin-top: 0;
            margin-bottom: 15px;
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
        }
        .skill-list {
            list-style: none;
            padding: 0;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
        }
        .skill-item a {
            display: block;
            background-color: #2a2a35;
            color: #fff;
            text-decoration: none;
            padding: 15px;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-weight: bold;
            text-align: center;
            border: 1px solid #333;
        }
        .skill-item a:hover {
            background-color: var(--accent-color);
            color: #fff;
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(255, 0, 127, 0.4);
            border-color: var(--accent-color);
        }
        footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: #666;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>TinCLE Talent Chips</h1>
        <div class="subtitle">Game Engine of the AI, by the AI, for the AI.</div>
"""

    if not versions:
        html_content += "<p style='text-align:center;'>No version directories found.</p>"

    for version_dir in versions:
        # 'version018' -> 'TinCLE Version 0.18' みたいに整形
        formatted_version = re.sub(r'version0*(\d)(\d{2})', r'TinCLE Version \1.\2', version_dir)
        # もしフォーマットに合わなかったら（例: version1）そのまま数字を使う
        if formatted_version == version_dir:
            num = version_dir.replace("version", "")
            try:
                # 001 -> 0.01 のように変換
                formatted_version = f"TinCLE Version {int(num)/100:.2f}"
            except ValueError:
                formatted_version = f"TinCLE {version_dir}"

        html_content += f"""
        <div class="version-section">
            <h2 class="version-title">{formatted_version}</h2>
            <ul class="skill-list">
"""

        # ディレクトリ内の .md ファイルを探す
        md_files = sorted([f for f in os.listdir(os.path.join(base_dir, version_dir)) if f.endswith('.md')])

        for md_file in md_files:
            file_path = f"{version_dir}/{md_file}"
            html_content += f"""                <li class="skill-item"><a href="{file_path}">{md_file}</a></li>\n"""

        html_content += """            </ul>
        </div>
"""

    html_content += """
    </div>
    <footer>
        &copy; 2026 michyo (Michiyo Tagami) - Created with General Assistant: Gyaru Sono
    </footer>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✨ index.html の生成が完了したよ！最高にアガるページになってるから確認してみて！💅")

if __name__ == "__main__":
    generate_index_html()
