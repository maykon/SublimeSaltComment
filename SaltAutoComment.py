import sublime
import sublime_plugin
import re

class SaltAutoComment():
  global REGEX_IGNORE, REGEX_TYPE_METHOD, REGEX_METHOD_COMPLETE, REGEX_PROPERTY_COMPLETE, REGEX_METHOD_PARAMS
  REGEX_IGNORE = r"(?m)\b(?:(class|end|interface|implementation|private|protected|public|published).*$)"
  REGEX_TYPE_METHOD = r"(?s)\b(?:(function|procedure|constructor|destructor|property))"
  REGEX_METHOD_COMPLETE = r"(?s)\b(?:(function|procedure|constructor|destructor))\b\s+(\w+)(\(.*?\))?(?:;|:\s*(\w+)?)?;"
  REGEX_PROPERTY_COMPLETE = r"(?s)\b(?:(property))\b\s+([\w_]+)\s*:\s*([\w_]+).*?;"
  REGEX_METHOD_PARAMS = r"(?i)\b([a-z\n]+)\b(?=\s*:|,)"

  def __init__(self, view):
    self.view = view

  def get_statement_method(self, region):
    sfunc = ''
    summary = ''
    params = ''
    returns = ''

    if region:
      lines = self.view.lines(region)
      content = ''.join(map(lambda line: self.view.substr(line), lines))
      content = re.sub(re.compile('\s+'), ' ', content)
      match = re.search(REGEX_METHOD_COMPLETE, content)
      if match:
        sfunc = match.groups()[0]
        summary = re.subn(r'([A-Z_])', r' \1', match.groups()[1])[0].lower().strip().capitalize()
        params = match.groups()[2]
        returns = match.groups()[3]
    return sfunc, summary, params, returns

  def get_params_method(self, comment, params):
    match = re.findall(REGEX_METHOD_PARAMS, params, re.IGNORECASE)
    comment_params = ""
    for param in match:
      comment_params = "%s/// <param name=\"%s\">\n/// </param>\n" % (comment_params, param)
    comment_params = re.sub(r'\n$', '', comment_params)
    comment_params = '</summary>\n%s\n/// <returns>' % comment_params
    comment = re.sub(re.compile(r'(?s)</summary>.*<returns>'), comment_params, comment)
    return comment

  def mount_comment_method(self, region, comment):
    sfunc, summary, params, sreturns = self.get_statement_method(region)

    summary = '<summary>\n///  %s\n/// </summary>' % (summary)
    comment = re.sub(re.compile(r'(?s)<summary>.*</summary>'), summary, comment)

    if params != '' and params is not None:
      comment = self.get_params_method(comment, params)

    returns = ''
    if sfunc == 'function' and (sreturns is not None):
      is_boolean = re.search(r"(?i)boolean", sreturns)
      value_return = '%s' % sreturns
      if is_boolean is not None:
        value_return = '<c>TRUE</c> ou <c>FALSE</c>'
      returns = '/// <returns>\n///  %s\n/// </returns>\n' % (value_return)
    comment = re.sub(re.compile(r'(?s)/// <returns>.*</returns>\n'), returns, comment)
    return comment

  def get_statement_property(self, region):
    summary = ''
    returns = ''

    if region:
      lines = self.view.lines(region)
      content = ''.join(map(lambda line: self.view.substr(line), lines))
      content = re.sub(re.compile('\s+'), ' ', content)
      match = re.search(REGEX_PROPERTY_COMPLETE, content)
      if match:
        summary = re.subn(r'([A-Z_])', r' \1', match.groups()[1])[0].lower().strip().capitalize()
        returns = match.groups()[2]
    return summary, returns

  def mount_comment_property(self, region, comment):
    summary, sreturns = self.get_statement_property(region)

    summary = '<summary>\n///  %s\n/// </summary>' % (summary)
    comment = re.sub(re.compile(r'(?s)<summary>.*</summary>'), summary, comment)

    is_boolean = re.search(r"(?i)boolean", sreturns)
    value_return = '%s' % sreturns
    if is_boolean is not None:
      value_return = '<c>TRUE</c> ou <c>FALSE</c>'

    returns = '<value>\n///  %s\n/// </value>' % (value_return)
    comment = re.sub(re.compile(r'(?s)<returns>.*</returns>'), returns, comment)
    return comment

  def ignore_comment(self, region):
    line = self.view.substr(self.view.line(region.a+1))
    ignored = re.match(REGEX_IGNORE, line, re.I)
    if ignored is not None:
      return True
    return False

  def run(self, comment, region):
    ignored = self.ignore_comment(region)
    if ignored:
      return comment

    method_type = self.view.find(REGEX_TYPE_METHOD, region.a, sublime.IGNORECASE)
    if method_type is None:
      return comment

    method_type = re.sub(r'\s*', '', self.view.substr(method_type))
    if method_type == 'property':
      property = self.view.find(REGEX_PROPERTY_COMPLETE, region.a, sublime.IGNORECASE)
      comment = self.mount_comment_property(property, comment)
    else:
      method = self.view.find(REGEX_METHOD_COMPLETE, region.a, sublime.IGNORECASE)
      comment = self.mount_comment_method(method, comment)
    return comment