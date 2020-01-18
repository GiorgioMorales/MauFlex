# -*- mode: python -*-

block_cipher = None

added_files=[('los_logos','los_logos'), ('Redes','Redes'), ('funciones_aguaje.py','.')]

a = Analysis(['MAUFLEX.py'],
             pathex=['E:\\INICTEL\\AguajesDeep\\Interfaz'],
             binaries=[],
             datas=added_files,
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
          exclude_binaries=True,
          name='MAUFLEX',
          debug=False,
          strip=False,
          upx=True,
          console=False,
		  icon = 'E:\\INICTEL\\AguajesDeep\\Interfaz\\los_logos\\inictelico.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='MAUFLEX')
