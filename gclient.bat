@echo off
:: Copyright (c) 2009 The Chromium Authors. All rights reserved.
:: Use of this source code is governed by a BSD-style license that can be
:: found in the LICENSE file.

:: This file is a stub to sync .\bootstrap first and defer control to
:: .\bootstrap\gclient.bat, which will sync back '.'. This is unless auto
:: update is disabled, were gclient.py is directly called.

:: Shall skip automatic update?
IF "%DEPOT_TOOLS_UPDATE%" == "0" GOTO :SKIP_UPDATE
:: We can't sync if .\.svn\. doesn't exist.
IF NOT EXIST "%~dp0.svn" GOTO :SKIP_UPDATE

:: Will download svn and python if not already installed on the system.
call "%~dp0bootstrap\win\win_tools.bat"
if errorlevel 1 goto :EOF

:: Sync the bootstrap directory *only after*.
call svn up -q "%~dp0bootstrap"
:: still continue even in case of error.
goto :UPDATE


:SKIP_UPDATE
:: Don't bother to try to update any thing.
python "%~dp0\gclient.py" %*
goto :EOF


:UPDATE
:: Transfer control to ease the update process. The following lines won't be
:: executed so don't add any! Specifically, don't use 'call' in the following
:: line.
"%~dp0bootstrap\gclient.bat" %*
goto :EOF