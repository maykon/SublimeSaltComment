# SublimeSaltComment
Sublime Text 3: Salt comment in Delphi files

## Usage

 - Simply hit `Ctrl+Shift+Alt+S` (on Windows and Linux) or `⌘+Shift+Alt+S` (on OS X) to create a simple salt comment in Delphi files
 - Simply hit `Ctrl+Shift+Alt+D` (on Windows and Linux) or `⌘+Shift+Alt+D` (on OS X) to create a method/property salt comment in Delphi files
 - Or you can open it via `Command Palette`, hit `Ctrl+Shift+P` and choose `Insert SALT Comment` or `Insert method/property SALT Comment`

## Installation

To install this plugin, you have two options:

1. If you have Package Control installed, simply search for `SublimeSaltComment` to install.

2. Clone source code to Sublime Text packages folder.

## Settings

This plugin has a three settings. If you create a file called `SublimeTnsNames.sublime-settings` in your `User` package you can override them.

``` JSON
{
   "user_name": "Maykon.db1",
   "auto_comment": true,
   "last_saltnumber": "253823/1",
   "last_rtcnumber": "12345"
}
```

## Examples


1. Simple salt comment

```
// 30/01/2018 - Maykon.db1 - SALT: 253823/1 - RTC: 12345
procedure TProcessadorPedido.MontarSelectProcessamentoDocumentos(const psTipoParte: string);
```

2. Method salt comment

```
/// <summary>
///  Monta o select de processamento de documentos
/// </summary>
/// <param name="psTipoParte">
/// </param>
/// <remarks>
///  30/01/2018 - Maykon.db1 - SALT: 253823/1 - RTC: 12345
/// </remarks>
procedure MontarSelectProcessamentoDocumentos(const psTipoParte: string);
```

3. Property salt comment

```
/// <summary>
///  Define o código do processo
/// </summary>
/// <value>
///  Integer
/// </value>
/// <remarks>
///  30/01/2018 - Maykon.db1 - SALT: 253823/1 - RTC: 12345
/// </remarks>
property CodigoProcesso: Integer read FnCdProcesso write SetCdProcesso;
```

