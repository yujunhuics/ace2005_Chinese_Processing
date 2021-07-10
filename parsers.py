from xml.etree import ElementTree
from bs4 import BeautifulSoup
import nltk
import json
import re


class Parsers:
    def __init__(self, path):
        self.entity_mentions = []
        self.event_mentions = []
        self.sentences = []

        self.entity_mentions, self.event_mentions = self.parse_xml(path + '.apf.xml')
        self.sents_with_pos = self.parse_sgm(path + '.sgm')

    @staticmethod
    def clean_text(text):
        text = text.replace('\n', ' ')
        return text

    def get_data(self):
        data = []

        def clean_text(text):
            text = text.replace('\n', ' ')
            return text

        for sent in self.sents_with_pos:
            item = dict()

            item['sentence'] = clean_text(sent['text'])
            item['position'] = sent['position']
            text_position = sent['position']

            for i, s in enumerate(item['sentence']):
                if s != ' ':
                    item['position'][0] += i
                    break
            item['sentence'] = item['sentence'].strip()

            entity_map = dict()
            item['golden-entity-mentions'] = []
            item['golden-event-mentions'] = []

            for entity_mention in self.entity_mentions:
                entity_position = entity_mention['position']
                if text_position[0] <= entity_position[0] and entity_position[1] <= text_position[1]:
                    item['golden-entity-mentions'].append({
                        'text': clean_text(entity_mention['text']),
                        'phrase-type': entity_mention['phrase-type'],
                        'position': entity_position,
                        'entity-type': entity_mention['entity-type'],
                    })
                    entity_map[entity_mention['entity-id']] = entity_mention

            for event_mention in self.event_mentions:
                event_position = event_mention['trigger']['position']
                if text_position[0] <= event_position[0] and event_position[1] <= text_position[1]:
                    event_arguments = []
                    for argument in event_mention['arguments']:
                        try:
                            entity_type = entity_map[argument['entity-id']]['entity-type']
                        except KeyError:
                            print('[Warning] The entity in the other sentence is mentioned. This argument will be ignored.')
                            continue

                        event_arguments.append({
                            'role': argument['role'],
                            'position': argument['position'],
                            'entity-type': entity_type,
                            'text': self.clean_text(argument['text']),
                        })

                    item['golden-event-mentions'].append({
                        'trigger': event_mention['trigger'],
                        'arguments': event_arguments,
                        'position': event_position,
                        'event_type': event_mention['event_type'],
                    })

            data.append(item)
        return data

    @staticmethod
    def parse_sgm(sgm_path):
        with open(sgm_path, 'r',encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), features='html.parser')
            sgm_text = soup.text

            doc_type = soup.doc.doctype.text.strip()

            def remove_tags(selector):
                tags = soup.findAll(selector)
                for tag in tags:
                    tag.extract()

            if doc_type == 'WEB TEXT':
                remove_tags('poster')
                remove_tags('postdate')
                remove_tags('subject')
            elif doc_type in ['CONVERSATION', 'STORY']:
                remove_tags('speaker')

            converted_text = soup.text
            # converted_text = converted_text.replace(' ill. ', ' ill ')
            # for sent in nltk.sent_tokenize(converted_text):
            #     sents.extend(re.split('[\n\n．]', sent))
            sents = re.split('。|！|\!|\n\n|？|\?', converted_text)
            sents = list(filter(lambda x: len(x) > 5, sents))
            sents = sents[1:]
            sents_with_pos = []
            last_pos = 0
            texts = [word for word in sgm_text]
            for sent in sents:
                sent =sent.strip()
                pos = sgm_text.find(sent, last_pos)
                last_pos = pos
                sents_with_pos.append({
                    'text': sent,
                    'position': [pos, pos + len(sent)]
                })

            return sents_with_pos

    def parse_xml(self, xml_path):
        entity_mentions, event_mentions = [], []
        tree = ElementTree.parse(xml_path)
        root = tree.getroot()

        for child in root[0]:
            if child.tag == 'entity':
                entity_mentions.extend(self.parse_entity_tag(child))
            elif child.tag in ['value', 'timex2']:
                entity_mentions.extend(self.parse_value_timex_tag(child))
            elif child.tag == 'event':
                event_mentions.extend(self.parse_event_tag(child))

        return entity_mentions, event_mentions

    @staticmethod
    def parse_entity_tag(node):
        entity_mentions = []

        for child in node:
            if child.tag != 'entity_mention':
                continue
            extent = child[0]
            charset = extent[0]

            entity_mention = dict()
            entity_mention['entity-id'] = child.attrib['ID']
            entity_mention['phrase-type'] = child.attrib['TYPE']
            entity_mention['entity-type'] = '{}:{}'.format(node.attrib['TYPE'], node.attrib['SUBTYPE'])
            entity_mention['text'] = charset.text
            entity_mention['position'] = [int(charset.attrib['START']), int(charset.attrib['END'])]

            entity_mentions.append(entity_mention)

        return entity_mentions

    @staticmethod
    def parse_event_tag(node):
        event_mentions = []
        for child in node:
            if child.tag == 'event_mention':
                event_mention = dict()
                event_mention['event_type'] = '{}:{}'.format(node.attrib['TYPE'], node.attrib['SUBTYPE'])
                event_mention['arguments'] = []
                for child2 in child:
                    if child2.tag == 'ldc_scope':
                        charset = child2[0]
                        event_mention['text'] = charset.text.replace('\n', ' ')
                        event_mention['position'] = [int(charset.attrib['START']), int(charset.attrib['END'])]
                    if child2.tag == 'anchor':
                        charset = child2[0]
                        event_mention['trigger'] = {
                            'text': charset.text.replace('\n', ' '),
                            'position': [int(charset.attrib['START']), int(charset.attrib['END'])],
                        }
                    if child2.tag == 'event_mention_argument':
                        extent = child2[0]
                        charset = extent[0]
                        if 'Time-' in child2.attrib['ROLE']:
                            Role = 'Time'
                        else:
                            Role = child2.attrib['ROLE']
                        event_mention['arguments'].append({
                            'text': charset.text,
                            'position': [int(charset.attrib['START']), int(charset.attrib['END'])],
                            'role': Role,
                            'entity-id': child2.attrib['REFID']
                        })
                event_mentions.append(event_mention)
        return event_mentions

    @staticmethod
    def parse_value_timex_tag(node):
        entity_mentions = []

        for child in node:
            extent = child[0]
            charset = extent[0]

            entity_mention = dict()
            entity_mention['entity-id'] = child.attrib['ID']

            if 'TYPE' in node.attrib:
                entity_mention['entity-type'] = node.attrib['TYPE']
                entity_mention['phrase-type'] = 'NUM'
            if 'SUBTYPE' in node.attrib:
                entity_mention['entity-type'] += ':{}'.format(node.attrib['SUBTYPE'])
            if child.tag == 'timex2_mention':
                entity_mention['entity-type'] = 'TIM:time'
                entity_mention['phrase-type'] = 'TIM'

            entity_mention['text'] = charset.text
            entity_mention['position'] = [int(charset.attrib['START']), int(charset.attrib['END'])]

            entity_mentions.append(entity_mention)

        return entity_mentions


if __name__ == '__main__':
    #data = Parser('./data/ace_2005_td_v7/data/test_example/AFP_ENG_20030616.0715').get_data()

    data = Parsers('./data/ace_2005_td_v7/data/Chinese/bn/adj/CNR20001201.1700.0558').get_data()
    with open('output/sample.jl', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
