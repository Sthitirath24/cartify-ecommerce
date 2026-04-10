@echo off
setlocal
set "NODE_HOME=%~dp0.local\node-v20.19.5-win-x64"
"%NODE_HOME%\node.exe" %*
