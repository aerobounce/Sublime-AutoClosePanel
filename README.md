# Auto Close Panel

### Small QoL improvement for Sublime Text

Hide unneeded output panels automatically on save, with regular expressions.

![](https://img.shields.io/badge/Platform-Linux%20/%20macOS%20/%20Windows-blue.svg)
![](https://img.shields.io/badge/Sublime%20Text-3+-orange.svg)

## Install

Clone this repository to `.../Sublime Text/Packages/`.

## Commands

### Close Panel

Close panel manually using patterns in settings.\
You can disable close on save feature and bind this command to a key instead.

### Print Panel Names to Console

Print name of available output panels.

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
