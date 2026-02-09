# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['pyqt_ui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Debug/OBC_FAULT_LOGIC.exe', 'Debug'),  # OBC_FAULT_LOGIC.exe 포함
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PySide6', 'PySide2', 'torch', 'tensorflow', 'scipy', 'IPython', 'sphinx', 'notebook', 'jupyterlab'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='OBC_Fault_Diagnostic_Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 콘솔 창 표시 (디버그용, 나중에 False로 변경 가능)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
