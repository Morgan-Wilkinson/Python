# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Web Novel Downloader.py', 'webNovelDownloaderInterface.py'],
             pathex=['/Users/morgan/Desktop/Web Novel Downloader'],
             binaries=[],
             datas=[],
             hiddenimports=['pdfkit', 'PyPDF2'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Web Novel Downloader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Web Novel Downloader')
app = BUNDLE(coll,
             name='Web Novel Downloader.app',
             icon="/Users/morgan/Desktop/Web Novel Downloader/icon.icns",
             bundle_identifier=None,
             info_plist={'NSHighResolutionCapable': 'True'},)
