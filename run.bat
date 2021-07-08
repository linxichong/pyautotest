
@echo off
chcp 65001
echo 开始打包
rd .\dist /S /Q
rd .\build /S /Q
pyinstaller autotest.py -F -w -i favicon.ico
echo 开始复制资源文件
xcopy .\drivers .\dist\drivers\ /e /y
xcopy .\flowdata .\dist\flowdata\ /e /y
xcopy .\mockdata .\dist\mockdata\ /e /y
xcopy .\proxy .\dist\proxy\ /e /y
copy autotest.yml .\dist\
copy const.yml .\dist\
copy README.md .\dist\
copy proxy.zip .\dist\
copy favicon.ico .\dist\
md .\dist\pic\
echo 打包完成