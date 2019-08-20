# -*- mode: python -*-

block_cipher = None


a = Analysis(['kinematix_special_search_script.py'],
             pathex=['D:\\_Projects\\python\\_my_github\\automate-google-search-script'],
             binaries=[],
             datas=[('resource', 'resource')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='kinematix_special_search_script',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
