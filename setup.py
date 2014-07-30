#!/usr/bin/python
import sys
import os
import sfml
from cx_Freeze import setup, Executable

includefiles = []
includes = ["numbers","re"]
excludes = ["sfml"]
packages = []

setup(
    name = "Project Dungeon",
    version = "0.0",
    description = "A game...",
    author = "Sicklebender",
    author_email = "tool@me.com",
    options = {'build_exe': {'includes':includes,'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [Executable("main.py", base = "Win32GUI")])