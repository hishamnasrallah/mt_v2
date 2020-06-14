import xml.etree.ElementTree as ET

from tqdm import tqdm
import requests
from mt_final.celery import app
from django.conf import settings
from translation.models import FileTranslation
from pusher import Pusher


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('(<.2*})|({.2*>)')

    # '<.*?>',
    return re.sub(clean, '', text)


def translate_ureed(source):
    print(source)

    print("notags")

    source = remove_html_tags(source)
    print(source)
    url = settings.SEGMENTATION_ENDPOINT_EN
    # url = "http://127.0.0.1:1200/api/segmented_translation"
    querystring = {"type": 's', "key": 'PPAS1HtVz13Y4q9xoJ0ooy6lr1543QmWvZM7Z690', "text": source}
    response = requests.request("POST", url, json=querystring)
    result = response.json()
    result = result['translation']
    # contents = urllib.request.urlopen(url + source_coded).read()
    # print(contents)
    #         break
    #     except:
    #         if i == 4:
    #             raise
    #         time.sleep(2)
    # # content_encoded = encodings.utf_8.decode(contents)[0]
    # print("content_encoded")
    # print(content_encoded)
    # json_result = json.loads(content_encoded, encoding='utf-8')
    # print("json_result")
    # print(json_result)
    # results = []
    # for result in json_result['Arabic_text']:
    #     results.append(result[1].replace('</s>', '').strip())
    # print(result)
    return result

@app.task()
def parsing_mxliff(file, file_translation_id):
    file = file
    tree = ET.parse(file)
    root = tree.getroot()
    # if 1 == 2:
    ns = {'m': "http://www.memsource.com/mxlf/2.0", 'units': "urn:oasis:names:tc:xliff:document:1.2"}
    transunits = root.findall('units:file/units:body/units:group/units:trans-unit', ns)
    for transunit in tqdm(transunits):
        # print(transunit)
        source = transunit.find('units:source', ns).text
        transunit.find('units:target', ns).text = translate_ureed(source)
    ET.register_namespace("", "urn:oasis:names:tc:xliff:document:1.2")
    ET.register_namespace('m', "http://www.memsource.com/mxlf/2.0")
    tree.write(file, encoding='utf-16')
    file_record = FileTranslation.objects.get(id=file_translation_id)
    file_record.status = "completed"
    file_record.save()
    file_name = str(file_record.file_en).split('/')[1]

    pusher = Pusher(app_id=u'943391', key=u'6891290613c25dda3ef1', secret=u'324b7ac7c8ff70315935',
                    cluster=u'mt1')
    print("file_name")
    print(file_name)
    print(file_name)
    pusher.trigger(f'my-channel-{file_record.updated_by.id}', 'my-event', {'message': f'file {file_name} translated'})

# celery -A Demo_translate worker --loglevel=info
