# coding:utf-8 

YML=".github/workflows/circle_translate.yml"

f = open(YML, "r+", encoding="UTF-8")
list1 = f.readlines()           
list1[7] = "   - cron: '0 * * * *'\n"

f = open(YML, "w+", encoding="UTF-8")
f.writelines(list1)
f.close()
