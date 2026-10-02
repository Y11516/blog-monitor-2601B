import json
import requests
import os
from datetime import datetime

# --- 核心配置区（已包含全班 34 位同学的信息） ---
# url: 博客网页真实地址
# repo: GitHub 仓库路径（用户名/仓库名），用于调用 API 抓取数据
# include_keywords: 白名单，留空 [] 代表只要不是黑名单里的都算作文章。
# exclude_keywords: 黑名单，包含这些词的路径或文件（如 readme, tags）不会被计入文章数。
BLOGS_CONFIG = [
    {"name": "李晓峰", "url": "https://yes-uisi.github.io/lxf", "repo": "yes-uisi/lxf", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "郭梓文", "url": "https://gz2008.github.io/task01/", "repo": "gz2008/task01", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "刘璧瑞", "url": "https://12128848.github.io", "repo": "12128848/12128848.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "周润祥", "url": "https://zrx-wyx.github.io", "repo": "zrx-wyx/zrx-wyx.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "闫凯峰", "url": "https://yankaifeng70-bot.github.io", "repo": "yankaifeng70-bot/yankaifeng70-bot.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "刘欣赢", "url": "http://eclair-tracy.github.io", "repo": "eclair-tracy/eclair-tracy.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "何芊宏", "url": "https://heqianhong1114.github.io/myblog/", "repo": "heqianhong1114/myblog", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "刘家怡", "url": "http://gysbfff.github.io", "repo": "gysbfff/gysbfff.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "路博雄", "url": "https://goldfish1232123.github.io/", "repo": "goldfish1232123/goldfish1232123.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "宋疏桐", "url": "", "repo": "", "branch": "main", "include_keywords": [], "exclude_keywords": []}, # 没填网址，跳过
    {"name": "贺佳琪", "url": "https://cecilia-scintilla.github.io/", "repo": "cecilia-scintilla/cecilia-scintilla.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "赵睿轩", "url": "https://zxy-wx-007.github.io/", "repo": "zxy-wx-007/zxy-wx-007.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "童杰瑞", "url": "https://rabit222.github.io/", "repo": "rabit222/rabit222.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "张宇晗", "url": "https://zhangyuhan1214.github.io/", "repo": "zhangyuhan1214/zhangyuhan1214.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "魏紫钰", "url": "https://Y11516.github.io", "repo": "Y11516/Y11516.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "佟奕轩", "url": "https://12eternity31.github.io/", "repo": "12eternity31/12eternity31.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "王嘉宝", "url": "https://wangjiabao711815.github.io/", "repo": "wangjiabao711815/wangjiabao711815.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "周璟", "url": "https://novaisntnova.github.io/", "repo": "novaisntnova/novaisntnova.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "张奕菲", "url": "https://Makerzyf.github.io/", "repo": "Makerzyf/Makerzyf.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "李梦涵", "url": "https://adelinecui.github.io/", "repo": "adelinecui/adelinecui.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "艾小杭", "url": "https://aixiaohang.github.io/", "repo": "aixiaohang/aixiaohang.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "王冠壹", "url": "https://wgy0828.github.io/wgy0828/", "repo": "wgy0828/wgy0828", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "王博昱", "url": "https://wby071115.github.io/", "repo": "wby071115/wby071115.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "李昊阳", "url": "https://02057.github.io/", "repo": "02057/02057.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "陈禹含", "url": "https://girwoft.github.io/", "repo": "girwoft/girwoft.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "王允恒", "url": "https://buu-yun.github.io/", "repo": "buu-yun/buu-yun.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "彭紫宸", "url": "https://pzc615156.github.io/", "repo": "pzc615156/pzc615156.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "王鹏绮", "url": "https://wpq-coder.github.io/pengqi.github.io/", "repo": "wpq-coder/pengqi.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "邓博元", "url": "https://buu2026sec078k.github.io/", "repo": "buu2026sec078k/buu2026sec078k.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "孙旌博", "url": "https://xysjb1-create.github.io/xysjb1/", "repo": "xysjb1-create/xysjb1", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "王远鹏", "url": "https://xiadie174.github.io/xiadie-s-/", "repo": "xiadie174/xiadie-s-", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "黄森豪", "url": "", "repo": "", "branch": "main", "include_keywords": [], "exclude_keywords": []}, # 没填网址，跳过
    {"name": "张绍勇", "url": "https://zhshy-chi.github.io", "repo": "zhshy-chi/zhshy-chi.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]},
    {"name": "孙家诚", "url": "https://eternity33313.github.io", "repo": "eternity33313/eternity33313.github.io", "branch": "main", "include_keywords": [], "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]}
]
# --- 配置结束 ---

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if os.environ.get('GITHUB_TOKEN'):
    HEADERS["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"

def get_blog_post_count(repo, branch, include_keywords, exclude_keywords):
    if not repo:
        return 0 # 处理没有填写仓库的同学
        
    url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15) 
        response.raise_for_status() 
        data = response.json()
        
        tree = data.get('tree', [])
        count = 0
        
        for item in tree:
            if item['type'] != 'blob': continue
            path = item['path'].lower()
            
            if not (path.endswith('.md') or path.endswith('.html')): continue
            if any(ex in path for ex in exclude_keywords): continue
            if include_keywords:
                if not any(kw.lower() in path for kw in include_keywords): continue
                    
            count += 1
            
        return count
    except Exception as e:
        print(f"  [错误] 获取 {repo} 数据失败: {e}")
        return 0

def main():
    results = []
    for blog in BLOGS_CONFIG:
        count = get_blog_post_count(
            blog["repo"], blog.get("branch", "main"),
            blog.get("include_keywords", []), blog.get("exclude_keywords", [])
        )
        results.append({
            "name": blog["name"], 
            "repo": blog["repo"] if blog["repo"] else "未填写",
            "url": blog.get("url", ""), 
            "count": count, 
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"{blog['name']}: {count} 篇")
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"blogs": results, "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
