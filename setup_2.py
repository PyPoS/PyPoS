from cx_Freeze import *
 
includefiles=["win32api.pyd","smaple.exe,"favicon.ico","pythoncom27.dll","pywintypes27.dll”,"images/cream_dust.png "]
excludes=[]
packages=[]
base = None
if sys.platform == "win32":
    base = "Win32GUI"
     
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Tool",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]\sample.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR",               # WkDir
     )
    ]
 
# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}
 
# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}
setup(
     version = "0.1",
     description = "Demo Tool",
     author = "Ashish",
     name = "Demo Tool",
     options = {'build_exe': {'include_files':includefiles}, "bdist_msi": bdist_msi_options,},
     executables = [
        Executable(
            script="sample.py",
            base=base,
            icon='favicon.ico',
            )
        ]
     )
