from cx_Freeze import setup, Executable

setup(
    name="LesMotsdeMaFoi",
    version="1.0",
    description="Mon jeu Python",
    executables=[Executable(r"c:\Jeu\InterfaceMotsdeMaFoi.py")]
)
