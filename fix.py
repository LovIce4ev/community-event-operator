with open("scripts/generate_poster.py", "r") as f:
    lines = f.readlines()

with open("scripts/generate_poster.py", "w") as f:
    for line in lines:
        if "ASSETS_DIR = os.path.join(BASE_DIR, \"assets\")" in line and "主标题" in line:
            f.write("        \"title\": os.path.join(ASSETS_DIR, \"主标题字体（江城黑体600W）.ttf\"),\n")
        elif "ASSETS_DIR = os.path.join(BASE_DIR, \"assets\")" in line and "副标题" in line and "zh" in line:
            pass # handled below
        elif "ASSETS_DIR =" in line and "副标题" in line:
            f.write("        \"info\": os.path.join(ASSETS_DIR, \"副标题及信息字体（江城黑体300W）.ttf\")\n")        
        elif "ASSETS_DIR = os.path.join(BASE_DIR, \"assets\")" in line and "Delight" in line and "Bold" in line:
            pass # we already have the fixed one below it
        elif "ASSETS_DIR = os.path.join(BASE_DIR, \"assets\")" in line and "Delight" in line and "Regular" in line:
            pass
        else:
            f.write(line)
