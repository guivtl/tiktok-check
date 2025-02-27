@echo off
title TikTok Block Checker
color 0f

python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0c
    echo Erro: Python nao encontrado! Por favor, instale o Python 3.8 ou superior.
    echo Voce pode baixar em: https://www.python.org/downloads/
    pause
    exit /b 1
)

if not exist requirements.txt (
    color 0c
    echo Erro: Arquivo requirements.txt nao encontrado!
    pause
    exit /b 1
)

if not exist config.json (
    color 0c
    echo Erro: Arquivo config.json nao encontrado!
    echo Por favor, crie o arquivo config.json com suas credenciais.
    pause
    exit /b 1
)

if not exist tiktok_cookies.json (
    color 0e
    echo Aviso: Arquivo de cookies nao encontrado!
    echo Voce precisara fazer login no TikTok na primeira execucao.
    echo.
    timeout /t 3 >nul
)

color 0e
echo Verificando dependencias...
pip install -r requirements.txt >nul 2>&1

cls

color 0f
python app.py

if %errorlevel% neq 0 (
    color 0c
    echo.
    echo O programa foi encerrado com um erro.
    pause
) 