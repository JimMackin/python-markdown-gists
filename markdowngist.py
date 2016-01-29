from markdown.preprocessors import Preprocessor
import re
from markdown.extensions import Extension

class MarkdownGist(Extension):
    def extendMarkdown(self, md, md_globals):
        #Register the Gist Preprocessor
        md.preprocessors.add('markdowngist',MarkdownGistPreprocessor(),'_begin')

class MarkdownGistPreprocessor(Preprocessor):
    def __init__(self):
		self.regex = re.compile('^\s*https?:\/\/gist\.github\.com\/\w+\/(\w+)\s*$')

    def get_gist(self, gist_id):
        url = "https://gist.githubusercontent.com/raw/{}".format(gist_id)
        import requests
        response = requests.get(url)

        if response.status_code != 200:
            return []
        body = response.text
        if not body:
            return []
        return body.splitlines()
    def run(self, lines):
        new_lines = []
        for line in lines:
            m = self.regex.match(line)
            if m:
                gist_id = m.group(1)
                new_lines.append('')
                new_lines.append('~~~~~')
                new_lines.extend(self.get_gist(gist_id))
                new_lines.append('~~~~~')
                new_lines.append('')
            else:
                new_lines.append(line)
        return new_lines
