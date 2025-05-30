# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('appCage.png', '.'), 
        ('style.qss', '.'),
        # (Opcional) inclua arquivos estáticos adicionais aqui
    ],
    hiddenimports=[
        # Flask + Werkzeug
        "flask", "werkzeug.serving",
        # Pandas / Excel
        "pandas", "openpyxl",
        # Cliente HTTP
        "requests",
        # PyQt6 internals (às vezes necessário)
        "PyQt6.QtCore", "PyQt6.QtGui", "PyQt6.QtWidgets"
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WheelCage App',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,               # <- Habilita console para ver erros
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['AppCage.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
