# RebarRIRToolkit

This is a toolkit for placing rebar using RhinoInside.Revit.

## Folder Organization
The project folder structure is as follows.
```
RebarRIRToolkit
│
├ README.md .. 
│
├ gh_scripts .. Code to use in GHPython.
│　├ 
～
│　└ ○○.py
│
├ my_package .. Modularized files
│　├ geometry .. Geometry-related
│　│　├ ○○.py
│　│　└ ○○.py
│　├ rebar .. Rebar-related
│　│　├ ○○.py
│　│　└ ○○.py
│　├ revit .. Revit-related
│　│　├ ○○.py
│　│　└ ○○.py
│　├ utils .. 
│　│　├ rhinoinside_utils.py : contains utility functions for using Rhino.Inside.
│　│　├ revit_utils.py : contains utility functions related to working with Revit.
│　│　└ grasshopper_utils.py : contains utility functions related to working with Grasshopper.
│　│　└ utils.py : contains utility general functions.
└ test .. GH file
　　├ ○○.gh
　　├ ○○.gh
　　└ ○○.gh
```
