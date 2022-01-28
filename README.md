# Auto Close Panel

### Small QoL improvement for Sublime Text

Hide unneeded output panels automatically on save, with regular expressions.

![](https://img.shields.io/badge/Platform-Linux%20/%20macOS%20/%20Windows-blue.svg)
![](https://img.shields.io/badge/Sublime%20Text-3+-orange.svg)

## Install

- Clone this repository to `.../Sublime Text/Packages/`.

## Commands

> **Command** is the name of the command you can use for **Key-Bindings**.

| Caption                                          | Command                         | Usage                                          |
| ------------------------------------------------ | ------------------------------- | ---------------------------------------------- |
| `Auto Close Panel: Test Patterns`                | `auto_close_panel_close`        | Check if patterns match without saving a file  |
| `Auto Close Panel: Print Panel Names to Console` | `auto_close_panel_print_panels` | Print name of available output panels          |

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
            ".*\\[(Finished.*?|Cancelled)\\]$"
        ]
    }
}
```
