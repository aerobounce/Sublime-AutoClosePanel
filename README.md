# Auto Close Panel

### Small QoL improvement for Sublime Text

Hide unneeded output panels automatically on save, with regular expressions.

[![](https://img.shields.io/badge/Platform-Linux%20/%20macOS%20/%20Windows-blue.svg)][packagecontrol]
[![](https://img.shields.io/badge/Sublime%20Text-3+-orange.svg)][packagecontrol]
[![](https://img.shields.io/github/v/tag/aerobounce/Sublime-AutoClosePanel?display_name=tag)][tags]

## Install

> Package Control: Currently waiting for PR to be merged

#### Manual Install

1. On terminal, move to the directory where you can open by `Preferences ▶ Browse Packages`
2. Clone this repository:

```sh
git clone "https://github.com/aerobounce/Sublime-AutoClosePanel.git" "Auto Close Panel"
```

## Commands

### Close Panel

- Close panel manually using patterns in settings.

### Print Panel Names to Console

- Print name of available output panels.

## Example

- Close Sublime LSP when no warning or errors are detected
- Close Build output panel when log ends with `Finished` or `Cancelled`

```json
{
    "target_panels": {
        // LSP diagnostics Panel
        "diagnostics": [
            "^\\s+No diagnostics. Well done!$"
        ],
        // Sublime Text Build output panel
        "exec": [
            ".*\\[(Finished in \\d+.*?|Cancelled|Finished)\\]$",
            ".*\\[Finished in \\d+.*? with exit code \\d+.*?\\].*",
        ]
    }
}
```

[tags]: https://github.com/aerobounce/Sublime-AutoClosePanel/tags
[packagecontrol]: https://github.com/aerobounce/Sublime-AutoClosePanel
