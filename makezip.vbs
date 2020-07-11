'**************************************************
' 压缩指定文件夹下所有文件
'
' ◆期待参数
'   1.文件夹路径 必须
'   2.zip文件名 必须
' ◆执行方式
'   > cscript makezip.vbs  文件夹路径  zip文件名
'**************************************************
Option Explicit


'**************************************************
' 常量定义
'**************************************************
Dim COMP_END_WAIT_MSEC
COMP_END_WAIT_MSEC = 3000


'**************************************************
'
' 变量定义
'
'**************************************************
Dim str
Dim Shell
Dim Fso
Dim WshShell
Dim objFolderPath
Dim objFolder
Dim Handle
Dim EmptyData
Dim strTargetZipFile
Dim objTargetFolder
Dim SINK
Dim objWMIService
Dim sv_counter
Dim counter
Dim ZipFile
Dim files
Dim file


'--------------------------------------------------
' 检查是否使用cscript.exe命令执行
'--------------------------------------------------
str = WScript.FullName
str = Right(str, 11)
str = Ucase(str)

if str <> "CSCRIPT.EXE" then
	WScript.Echo("error : Please use cscript.exe command to execute")
	WScript.Quit(-1)
end if


'--------------------------------------------------
' 检查参数是否存在
'--------------------------------------------------
if WScript.Arguments.Count <> 2 then
	WScript.Echo("error : Argument counts are invalid.")
	WScript.Quit(-1)
end if

' 获取参数
' 压缩目标文件夹
objFolderPath = WScript.Arguments(0)
' 压缩文件名
ZipFile   = WScript.Arguments(1)

'--------------------------------------------------
' 关键对象
'--------------------------------------------------
Set Shell    = WScript.CreateObject("Shell.Application")
Set Fso      = WScript.CreateObject("Scripting.FileSystemObject")
Set WshShell = WScript.CreateObject("WScript.Shell")

'--------------------------------------------------
' 删除既存压缩文件
'--------------------------------------------------
if fso.FileExists(ZipFile) then
	Fso.DeleteFile ZipFile, True
End if

'--------------------------------------------------
' 生成空压缩文件
'--------------------------------------------------
Set Handle = Fso.CreateTextFile(ZipFile, True)
EmptyData = Chr(&H50) & Chr(&H4B) & Chr(&H5) & Chr(&H6)
EmptyData = EmptyData & String(18, Chr(0))

Handle.Write EmptyData
Handle.Close

'--------------------------------------------------
' 循环目标文件夹下所有文件，依次放入压缩文件中
'--------------------------------------------------
Set objTargetFolder = Shell.NameSpace(Fso.GetAbsolutePathName(ZipFile))
Set objFolder = Fso.GetFolder(objFolderPath)
For Each file In objFolder.Files
	WScript.Echo(file)
	WScript.Echo(fso.GetAbsolutePathName(objFolderPath) & "\" & file.Name)
	objTargetFolder.CopyHere(fso.GetAbsolutePathName(objFolderPath) & "\" & file.Name)
Next

'--------------------------------------------------
' 每3秒判断压缩是否完结
'--------------------------------------------------
Do
	sv_counter = counter
	WScript.Sleep COMP_END_WAIT_MSEC
	if sv_counter = counter then
		WScript.Echo("Zip process is successful.")
		WScript.Quit(-1)
	end if
Loop