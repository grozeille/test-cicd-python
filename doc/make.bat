@echo off
setlocal

set SPHINXBUILD=sphinx-build
set SOURCEDIR=.
set BUILDDIR=_build

if "%1"=="html" (
  %SPHINXBUILD% -b html %SOURCEDIR% %BUILDDIR%\html
  goto :eof
)
if "%1"=="clean" (
  if exist %BUILDDIR% rd /s /q %BUILDDIR%
  goto :eof
)
echo Usage: make.bat [html|clean]
