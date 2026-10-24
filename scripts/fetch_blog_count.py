import json
import requests
import os
from datetime import datetime

# --- 配置靶场关键词（严格版，剔除宽泛词汇） ---
TARGETS_CONFIG = {
    "Bugku": ["bugku"],
    "CTFHub": ["ctfhub", "ctf_hub"], 
    "Pikachu": ["pikachu"],
    "SQLi-Labs": ["sqli-labs", "sqli_labs", "sqllibs", "less-"],
    "Upload-Labs": ["upload-labs", "upload_labs", "uploadlabs", "pass-"],
    "DVWA": ["dvwa"],
    "Burp-Labs": ["burp-labs", "burp_labs", "burplabs"],
    "RCE-Labs": ["rce-labs", "rce_labs", "rcelabs"],
    "单点靶场": ["single", "单点"]
}

# --- 全班同学配置（已根据最新截图补全所有 url 字段） ---
BLOGS_CONFIG = [
    
    {"name": "郭梓文", "repo": "gz2008/task01", "url": "https://gz2008.github.io/task01/", "branch": "main"},
    {"name": "刘璧瑞", "repo": "12128848/12128848.github.io", "url": "https://12128848.github.io", "branch": "main"},
    {"name": "周润祥", "repo": "zrx-wyx/zrx-wyx.github.io", "url": "https://zrx-wyx.github.io", "branch": "main"},
    {"name": "闫凯峰", "repo": "yankaifeng70-bot/yankaifeng70-bot.github.io", "url": "https://yankaifeng70-bot.github.io", "branch": "main"},
    {"name": "刘欣赢", "repo": "eclair-tracy/eclair-tracy.github.io", "url": "http://Eclair-Tracy.github.io", "branch": "main"},
    {"name": "何芊宏", "repo": "heqianhong1114/myblog", "url": "https://heqianhong1114.github.io/myblog/", "branch": "main"},
    {"name": "刘家怡", "repo": "gysbfff/gysbfff.github.io", "url": "http://gysbfff.github.io", "branch": "main"},
    {"name": "路博雄", "repo": "goldfish1232123/goldfish1232123.github.io", "url": "https://goldfish1232123.github.io/", "branch": "main"},
    # 10号 宋疏桐 (已补全)
    {"name": "宋疏桐", "repo": "song-86-ui/song-86-ui.github.io", "url": "https://song-86-ui.github.io/", "branch": "main"},
    {"name": "贺佳琪", "repo": "cecilia-scintilla/cecilia-scintilla.github.io", "url": "https://cecilia-scintilla.github.io/", "branch": "main"},
    {"name": "赵睿轩", "repo": "zxy-wx-007/zxy-wx-007.github.io", "url": "https://Zxy-wx-007.github.io/", "branch": "main"},
    {"name": "童杰瑞", "repo": "rabit222/rabit222.github.io", "url": "https://rabit222.github.io/", "branch": "main"},
    # 14号 张宇晗 (网址带子路径，仓库名取子路径名)
    {"name": "张宇晗", "repo": "zhangyuhan1214/zhangyuhan.github.io", "url": "https://zhangyuhan1214.github.io/zhangyuhan.github.io/", "branch": "main"},
    {"name": "魏紫钰", "repo": "Y11516/Y11516.github.io", "url": "https://Y11516.github.io", "branch": "main"},
    {"name": "佟奕轩", "repo": "12eternity31/12eternity31.github.io", "url": "https://12eternity31.github.io/", "branch": "main"},
    {"name": "王嘉宝", "repo": "wangjiabao711815/wangjiabao711815.github.io", "url": "https://wangjiabao711815.github.io/", "branch": "main"},
    {"name": "周璟", "repo": "novaisntnova/novaisntnova.github.io", "url": "https://novaisntnova.github.io/#/", "branch": "main"},
    {"name": "张奕菲", "repo": "Makerzyf/Makerzyf.github.io", "url": "https://Makerzyf.github.io/", "branch": "main"},
    {"name": "李梦涵", "repo": "adelinecui/adelinecui.github.io", "url": "https://adelinecui.github.io/", "branch": "main"},
    {"name": "艾小杭", "repo": "aixiaohang/aixiaohang.github.io", "url": "https://aixiaohang.github.io/", "branch": "main"},
    {"name": "王冠壹", "repo": "wgy0828/wgy0828", "url": "https://wgy0828.github.io/wgy0828/", "branch": "main"},
    {"name": "王博昱", "repo": "wby071115/wby071115.github.io", "url": "https://wby071115.github.io/", "branch": "main"},
    {"name": "李昊阳", "repo": "02057/02057.github.io", "url": "https://02057.github.io/", "branch": "main"},
    {"name": "陈禹含", "repo": "girwoft/girwoft.github.io", "url": "https://girwoft.github.io/", "branch": "main"},
    # 26号 王允恒 (接龙里填的是 github 仓库地址，自动转换成网页地址)
    {"name": "王允恒", "repo": "buu-yun/buu-yun.github.io", "url": "https://buu-yun.github.io/", "branch": "main"},
    {"name": "彭紫宸", "repo": "pzc615156/pzc615156.github.io", "url": "https://pzc615156.github.io/", "branch": "main"},
    {"name": "王鹏绮", "repo": "wpq-coder/pengqi.github.io", "url": "https://wpq-coder.github.io/pengqi.github.io/", "branch": "main"},
    {"name": "邓博元", "repo": "buu2026sec078k/buu2026sec078k.github.io", "url": "https://buu2026sec078k.github.io/", "branch": "main"},
    {"name": "孙旌博", "repo": "xysjb1-create/xysjb1", "url": "https://xysjb1-create.github.io/xysjb1/", "branch": "main"},
    {"name": "王远鹏", "repo": "xiadie174/xiadie-s-", "url": "https://xiadie174.github.io/xiadie-s-/", "branch": "main"},
    # 32号 黄森豪 (已补全)
    {"name": "黄森豪", "repo": "sen3-oil/sen3-oil.github.io", "url": "https://sen3-oil.github.io", "branch": "main"},
    {"name": "张绍勇", "repo": "zhshy-chi/zhshy-chi.github.io", "url": "https://zhshy-chi.github.io", "branch": "main"},
    {"name": "孙家诚", "repo": "eternity33313/eternity33313.github.io", "url": "https://eternity33313.github.io", "branch": "main"}
]

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if os.environ.get('GITHUB_TOKEN'):
    HEADERS["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"

def get_student_lab_counts(repo, branch):
    counts = {lab: 0 for lab in TARGETS_CONFIG.keys()}
    if not repo:
        return counts
        
    url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15) 
        response.raise_for_status() 
        data = response.json()
        
        tree = data.get('tree', [])
        for item in tree:
            if item['type'] != 'blob': continue
            path = item['path'].lower()
            
            if not (path.endswith('.md') or path.endswith('.html')): continue
            if any(ex in path for ex in ["index", "readme", "tags", "categories", "archives"]): continue
            
            for lab_name, keywords in TARGETS_CONFIG.items():
                if any(kw in path for kw in keywords):
                    counts[lab_name] += 1
                    break
        return counts
    except Exception as e:
        print(f"  [错误] 获取 {repo} 数据失败: {e}")
        return counts

def main():
    results = []
    for blog in BLOGS_CONFIG:
        counts = get_student_lab_counts(blog["repo"], blog.get("branch", "main"))
        total = sum(counts.values())
        
        results.append({
            "name": blog["name"], 
            "repo": blog["repo"] if blog["repo"] else "未填写",
            "url": blog.get("url", ""), # 关键：存入网址
            "stats": counts,
            "total": total
        })
        print(f"{blog['name']}: 总计 {total} 篇")
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"blogs": results, "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
