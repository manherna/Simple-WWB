:: Manuel Hernández (@manherna) 03/04/2020 ::
:: Script that packages all the necesary files to run the WW-BOT inside AWS Lambda ::
:: Generates a zip using 7zip comandline application ::

@echo off
set %TEMPDIR=.\tmp
set LIBSFOLDER=.\v-env\Lib\site-packages
mkdir %TEMPDIR%

rmdir /Q/S %LIBSFOLDER%\__pycache__
xcopy /s /E /I /Y %LIBSFOLDER% %TEMPDIR%
for %%i in (models.py logic.py persistence.py logger.py lambda_function.py) do xcopy /Y %%i %TEMPDIR%

"C:\Program Files\7-Zip\7z.exe" a UPLOAD.zip %TEMPDIR%\*

rmdir /Q/S %TEMPDIR%