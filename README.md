# FIT3077 Repository

File links:

Domain Model Justifications: https://docs.google.com/document/d/1yKH65VIyLR54c94-UZSKeysLO1F8Y0hoMnV8pnum_mQ/edit?tab=t.0#heading=h.jebknf66jved    
Team Information: https://docs.google.com/document/d/1gRtUwZf5ojBV6tBfpLvNhbWF_KGSl5Q9_PlUqk1xylg/edit?tab=t.0#heading=h.l7byjle2t2or   
User Stories: https://docs.google.com/document/d/1qGGDGRkIJO3NXx3LltwrCCSCGYfNwYLJSKhEABUDtuY/edit?tab=t.0#heading=h.39gcmxrbel6n   

# Build Instructions
## Requirements
- The repository
	- [.zip link](https://git.infotech.monash.edu/FIT3077/fit3077-s1-2025/assignment-groups/CL_Tuesday04pm_Team012/project/-/archive/main/project-main.zip)
- python (3.12 was used)
- pyinstaller
	- `pip install pyinstaller` ([See More](https://pyinstaller.org/en/stable/index.html))
## Build Steps (Windows)
### Auto
Run `build.bat`
### Manual
1) Ensure current directory is `./code/` (from top level: `cd ./code`)
2) Build `pyinstaller .\App.py --onefile --name Santorini --contents-directory Resources --hidden-import=tkinter --add-data ./Assets:Assets`
3) Run by clicking on the executable in `./dist` or `./dist/Santorini.exe`

# Better Comments
Extension: https://github.com/aaron-bond/better-comments

The following config was used (`better-comments.tags`):
```json
"better-comments.tags": [
    {
      "tag": "todo",
      "color": "#FF2D00",
      "strikethrough": false,
      "underline": false,
      "backgroundColor": "transparent",
      "bold": false,
      "italic": false
    },
    {
      "tag": "region",
      "color": "#067f5f",
      "strikethrough": false,
      "underline": false,
      "backgroundColor": "transparent",
      "bold": false,
      "italic": true
    },
    {
      "tag": "endregion",
      "color": "#067f5f",
      "strikethrough": false,
      "underline": false,
      "backgroundColor": "transparent",
      "bold": false,
      "italic": true
    },
    {
      "tag": "~",
      "color": "#bc0cfc",
      "strikethrough": false,
      "underline": false,
      "backgroundColor": "transparent",
      "bold": true,
      "italic": true
    },
    {
      "tag": "?",
      "color": "#fcbc0c",
      "strikethrough": false,
      "underline": false,
      "backgroundColor": "transparent",
      "bold": false,
      "italic": true
    },
    {
      "tag": "@",
      "color": "#3498DB",
      "strikethrough": false,
      "underline": false,
      "backgroundColor": "transparent",
      "bold": false,
      "italic": false
    },
    {
      "tag": "//",
      "color": "#474747",
      "strikethrough": true,
      "underline": false,
      "backgroundColor": "transparent",
      "bold": false,
      "italic": false
    },
    {
      "tag": "!",
      "color": "#FF8C00",
      "strikethrough": false,
      "underline": false,
      "backgroundColor": "transparent",
      "bold": false,
      "italic": false
    },
    {
      "tag": "*",
      "color": "#98C379",
      "strikethrough": false,
      "underline": false,
      "backgroundColor": "transparent",
      "bold": false,
      "italic": false
    },
    {
      "tag": "#",
      "color": "#a8a095",
      "strikethrough": false,
      "underline": false,
      "backgroundColor": "transparent",
      "bold": false,
      "italic": false
    }
]
```