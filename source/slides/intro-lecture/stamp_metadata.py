"""Retain ordinary authorship in a generated PowerPoint package.

Created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026.
Metadata is attribution, not a copy-protection or tracking mechanism.
"""
from pathlib import Path
import os
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET


def stamp(path):
    path = Path(path)
    if path.suffix.lower() == '.pdf':
        from pypdf import PdfWriter
        writer = PdfWriter(clone_from=str(path))
        writer.add_metadata({
            '/Author': 'Allamaprabhu Ani',
            '/Title': 'PhAST: Numerical methods and deep learning',
            '/Subject': 'CEMS-Lab, UKACM Autumn School 2026; '
                        'presented by Sathiskumar A. Ponnusami, Queen Mary University of London.',
        })
        fd, temp = tempfile.mkstemp(prefix='phast-metadata-', suffix='.pdf', dir=path.parent)
        os.close(fd)
        with open(temp, 'wb') as revised:
            writer.write(revised)
        writer.close()
        os.replace(temp, path)
        return
    ns = {'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties',
          'dc': 'http://purl.org/dc/elements/1.1/',
          'dcterms': 'http://purl.org/dc/terms/',
          'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    for key, uri in ns.items():
        ET.register_namespace(key, uri)
    with zipfile.ZipFile(path) as original:
        root = ET.fromstring(original.read('docProps/core.xml'))
        for name, value in {
            'creator': 'Allamaprabhu Ani',
            'description': 'CEMS-Lab course material, UKACM Autumn School 2026. '
                           'Created by Allamaprabhu Ani. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.',
        }.items():
            item = root.find('dc:' + name, ns)
            if item is None:
                item = ET.SubElement(root, '{' + ns['dc'] + '}' + name)
            item.text = value
        fd, temp = tempfile.mkstemp(prefix='phast-metadata-', suffix='.pptx', dir=path.parent)
        os.close(fd)
        with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as revised:
            for member in original.infolist():
                revised.writestr(member, ET.tostring(root, encoding='utf-8', xml_declaration=True)
                                 if member.filename == 'docProps/core.xml'
                                 else original.read(member.filename))
    os.replace(temp, path)


if __name__ == '__main__':
    stamp(sys.argv[1])
