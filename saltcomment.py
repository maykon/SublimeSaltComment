import sublime, sublime_plugin
import os

from datetime import datetime, date
import re

from SublimeSaltComment.SaltAutoComment import SaltAutoComment

class SaltCommentCommand(sublime_plugin.TextCommand):
  def run(self, edit, saltnumber=None, username=None, rtcnumber=None):

    s = sublime.load_settings("SublimeSaltComment.sublime-settings")
    user_name = s.get("user_name", username)
    if user_name is None or user_name == '':
      user_name = os.environ.get("USERNAME")

    last_user_name = s.get("last_user_name", user_name)
    if saltnumber is None:
      last_saltnumber = s.get("last_saltnumber", "")
      self.view.window().show_input_panel(
        "SALT Number:",
        str(saltnumber) if saltnumber else last_saltnumber,
        lambda f: self.view.run_command("salt_comment", {"saltnumber": f, 
          "username": last_user_name, "rtcnumber": None}),
        None, None
      )
      return

    if saltnumber is not None:
      if saltnumber == '' or not isinstance(saltnumber, str) or saltnumber.isspace():
        return

    if rtcnumber is None:
      rtc_number = s.get("last_rtcnumber", "")
      self.view.window().show_input_panel(
        "RTC Number:",
        str(rtcnumber) if rtcnumber else rtc_number,
        lambda f: self.view.run_command("salt_comment", {"saltnumber": saltnumber, 
          "username": last_user_name,  "rtcnumber": f}),
        None, None
      )
      return

    if rtcnumber is not None:
      if rtcnumber == '' or not isinstance(rtcnumber, str) or rtcnumber.isspace():
        return

    text = "// " + date.today().strftime("%d/%m/%Y") + " - " + user_name + " - SALT: " + saltnumber + " - RTC: " + rtcnumber

    s.set("last_saltnumber", saltnumber)
    s.set("user_name", user_name)
    s.set("last_rtcnumber", rtcnumber)
    sublime.save_settings("SublimeSaltComment.sublime-settings")

    for r in self.view.sel():
      if r.empty():
          self.view.insert(edit, r.a, text)
      else:
          self.view.replace(edit, r,   text)

class SaltHelpInsightCommentCommand(sublime_plugin.TextCommand):
  def run(self, edit, saltnumber=None, username=None, rtcnumber=None):

    s = sublime.load_settings("SublimeSaltComment.sublime-settings")
    user_name = s.get("user_name", username)
    if user_name is None or user_name == '':
      user_name = os.environ.get("USERNAME")

    last_user_name = s.get("last_user_name", user_name)
    if saltnumber is None:
      last_saltnumber = s.get("last_saltnumber", "")
      self.view.window().show_input_panel(
        "SALT Number:",
        str(saltnumber) if saltnumber else last_saltnumber,
        lambda f: self.view.run_command("salt_help_insight_comment", {"saltnumber": f, 
          "username": last_user_name, "rtcnumber": None}),
        None, None
      )
      return

    if saltnumber is not None:
      if saltnumber == '' or not isinstance(saltnumber, str) or saltnumber.isspace():
        return

    if rtcnumber is None:
      rtc_number = s.get("last_rtcnumber", "")
      self.view.window().show_input_panel(
        "RTC Number:",
        str(rtcnumber) if rtcnumber else rtc_number,
        lambda f: self.view.run_command("salt_help_insight_comment", {"saltnumber": saltnumber, 
          "username": last_user_name, "rtcnumber": f}),
        None, None
      )
      return

    if rtcnumber is not None:
      if rtcnumber == '' or not isinstance(rtcnumber, str) or rtcnumber.isspace():
        return

    text = "/// <summary>\n" \
      "///  \n" \
      "/// </summary>\n" \
      "/// <returns>\n" \
      "///  NONE\n" \
      "/// </returns>\n" \
      "/// <remarks>\n" \
      "///  " + date.today().strftime("%d/%m/%Y") + " - " + user_name + " - SALT: " + saltnumber + " - RTC: " + rtcnumber + "\n" \
      "/// </remarks>"

    use_auto_comment = s.get("auto_comment", True)
    s.set("last_saltnumber", saltnumber)
    s.set("user_name", user_name)
    s.set("auto_comment", use_auto_comment)
    s.set("last_rtcnumber", rtcnumber)
    sublime.save_settings("SublimeSaltComment.sublime-settings")

    if use_auto_comment:
      auto_comment = SaltAutoComment(self.view)

    for r in self.view.sel():
      if use_auto_comment:
        text = auto_comment.run(text, r)
      if r.empty():
        self.view.insert(edit, r.a, text)
      else:
        self.view.replace(edit, r, text)

class SaltUnitCommentCommand(sublime_plugin.TextCommand):
  def run(self, edit, saltnumber=None, username=None, rtcnumber=None, system=None, module=None, comment=None):

    s = sublime.load_settings("SublimeSaltComment.sublime-settings")
    user_name = s.get("user_name", username)
    if user_name is None or user_name == '':
      user_name = os.environ.get("USERNAME")

    last_user_name = s.get("last_user_name", user_name)
    if saltnumber is None:
      last_saltnumber = s.get("last_saltnumber", "")
      self.view.window().show_input_panel(
        "SALT Number:",
        str(saltnumber) if saltnumber else last_saltnumber,
        lambda f: self.view.run_command("salt_unit_comment", {"saltnumber": f, 
          "username": last_user_name, "rtcnumber": None}),
        None, None
      )
      return

    if saltnumber is not None:
      if saltnumber == '' or not isinstance(saltnumber, str) or saltnumber.isspace():
        return

    if rtcnumber is None:
      rtc_number = s.get("last_rtcnumber", "")
      self.view.window().show_input_panel(
        "RTC Number:",
        str(rtcnumber) if rtcnumber else rtc_number,
        lambda f: self.view.run_command("salt_unit_comment", {"saltnumber": saltnumber, 
          "username": last_user_name, "rtcnumber": f}),
        None, None
      )
      return

    if rtcnumber is not None:
      if rtcnumber == '' or not isinstance(rtcnumber, str) or rtcnumber.isspace():
        return

    if system is None:
      _system = s.get("last_system", "")
      self.view.window().show_input_panel(
        "System:",
        str(system) if system else _system,
        lambda f: self.view.run_command("salt_unit_comment", {"saltnumber": saltnumber, 
          "username": last_user_name, "rtcnumber": rtcnumber, "system": f}),
        None, None
      )
      return

    if system is not None:
      if system == '' or not isinstance(system, str) or system.isspace():
        return

    if module is None:
      _module = s.get("last_module", "")
      self.view.window().show_input_panel(
        "Module:",
        str(module) if module else _module,
        lambda f: self.view.run_command("salt_unit_comment", {"saltnumber": saltnumber, 
          "username": last_user_name, "rtcnumber": rtcnumber, "system": system, "module": f}),
        None, None
      )
      return

    if module is not None:
      if module == '' or not isinstance(module, str) or module.isspace():
        return

    if comment is None:
      _comment = s.get("last_comment", "")
      self.view.window().show_input_panel(
        "Objective:",
        str(comment) if comment else _comment,
        lambda f: self.view.run_command("salt_unit_comment", {"saltnumber": saltnumber, 
          "username": last_user_name, "rtcnumber": rtcnumber, "system": system, "module": module,
          "comment": f}),
        None, None
      )
      return

    if comment is not None:
      if comment == '' or not isinstance(comment, str) or comment.isspace():
        return

    text = "{*****************************************************************************\n" \
      " Projeto/Sistema: " + system + " / " + module + "\n" \
      " Objetivo: " + comment + "\n" \
      " Criação: " + date.today().strftime("%d/%m/%Y") + " - " + user_name + "\n" \
      " SALT: " + saltnumber + "\n" \
      " RTC: " + rtcnumber + "\n" \
      " *****************************************************************************}"

    s.set("last_saltnumber", saltnumber)
    s.set("user_name", user_name)
    s.set("last_rtcnumber", rtcnumber)
    s.set("last_system", system)
    s.set("last_module", module)
    s.set("last_comment", comment)
    sublime.save_settings("SublimeSaltComment.sublime-settings")

    for r in self.view.sel():
      if r.empty():
        self.view.insert(edit, r.a, text)
      else:
        self.view.replace(edit, r, text)