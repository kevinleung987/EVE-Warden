from cx_Freeze import setup, Executable

includefiles = ['config.json', 'alert.wav']
setup(name="EVE Warden",
      version="0.1",
      description="",
      options={'build_exe': {'include_files': includefiles}},
      executables=[Executable("evewarden.py"), Executable("calibrator.py")])
