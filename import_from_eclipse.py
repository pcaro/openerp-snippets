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
    <scope>source.python</scope>
</snippet>"""


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
        data = t.childNodes[0].data
        content = data.replace('${cr}', '$0')
        o = Replacer()
        content2 = replace_re.sub(o.replace, content)
        snippet = SNIPPET_TEMPLATE % dict(content=content2, name=name)
        fname = name + '.sublime-snippet'
        if os.path.exists(fname):
            print '%s ya existe'
        else:
            with open(fname, "w") as f:
                f.write(snippet)
                print '*' * 10
                print snippet

if __name__ == '__main__':
    main()
