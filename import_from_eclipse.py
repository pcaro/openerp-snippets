import string
import sys
import re
import os
from xml.dom import minidom

SNIPPET_TEMPLATE = """
<snippet>
    <content><![CDATA[
%(content)s
]]></content>
    <tabTrigger>%(name)s</tabTrigger>
    <scope>%(scope)s</scope>
    <description>%(description)s</description>
</snippet>"""


def slugify(value):
    """
    Normalizes string, for use as file name.
    """
    value = re.sub('[-\s]+', '_', value)
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in value if c in valid_chars)


class Replacer(object):
    def __init__(self):
        self.next = 1
        self.data = {}

    def number_of(self, name):
        if not name in self.data:
            self.data[name] = self.next
            self.next = self.next + 1
        return self.data[name]

    def replace(self, m):
        name = m.groups()[0]
        number = self.number_of(name)
        return '${%s:%s}' % (number, name)


def main():
    data = open(sys.argv[1]).read()
    document = minidom.parseString(data)
    replace_re = re.compile(r'\$\{(?P<var>\w*)\}')
    for t in document.getElementsByTagName('template'):
        name = t.getAttribute('name')
        context = t.getAttribute('context')
        description = t.getAttribute('description')
        scope = 'text'
        if 'python' in context:
            scope = 'source.python'
        if 'xml' in context:
            scope = 'text.xml'
        data = t.childNodes[0].data
        content = data.replace('${cr}', '$0')
        o = Replacer()
        content = replace_re.sub(o.replace, content)
        snippet = SNIPPET_TEMPLATE % dict(content=content, name=name, scope=scope,
                                          description=description)
        fname = slugify(name) + '.sublime-snippet'
        if os.path.exists(fname):
            print '%s exists' % fname
        else:
            with open(fname, "w") as f:
                f.write(snippet)
                print "%s generated" % fname

if __name__ == '__main__':
    main()
