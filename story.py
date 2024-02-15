import json
import os
from loguru import logger


class Chapter(dict):
    def __init__(self, index):
        super().__init__()
        self['index'] = index
        self['versions'] = []

    def add_version(self, tile, content):
        logger.info(f"Update version for chapter {self['index']}")
        self['versions'].append({'tile': tile, 'content': content})

    def as_str(self):
        current = self['versions'][-1]
        return f'{current["tile"]}\n{current["content"]}'


class Story(dict):
    def __init__(self):
        super().__init__()
        self['chapters'] = {}
        self['reviews'] = []

    def was_written(self) -> bool:
        return self['chapters']

    def add_chapter(self, chapter_id, tile, content):
        chapter_id = str(chapter_id)
        if 'chapters' not in self:
            self['chapters'] = {}
        if chapter_id not in self['chapters']:
            self['chapters'][chapter_id] = Chapter(chapter_id)

        self['chapters'][chapter_id].add_version(tile, content)
        self.save()

    def add_review(self, content):
        if 'reviews' not in self:
            self['reviews'] = []
        self['reviews'].append(content)
        self.save()

    def last_review(self):
        return self['reviews'][-1]

    def save(self, file_name='out/story.json'):
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(self, f, indent=2)

    def as_str(self):
        return '\n'.join([chapter.as_str() for chapter in self['chapters'].values()])

    @staticmethod
    def load(file_name):
        s = Story()

        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                d = json.load(f)
                s.update(d)
                for i, chap in d['chapters'].items():
                    s['chapters'][i] = Chapter(i)
                    s['chapters'][i].update(chap)
        return s


story = Story.load('out/story.json')
