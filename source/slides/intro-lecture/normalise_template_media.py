"""Normalise inherited template PNG encoding without changing slide content.

Created by Allamaprabhu Ani for CEMS-Lab, UKACM Autumn School 2026.
Only the three original high-depth template backgrounds are re-encoded.
Their slide-level backgrounds are overridden by the authored gradient/fills.
All nineteen visible scientific images must remain byte-identical.
"""
from io import BytesIO
from pathlib import Path
import hashlib
import json
import os
import sys
import tempfile
import zipfile
from PIL import Image, ImageCms


def normalise(path):
    path = Path(path)
    targets = {'ppt/media/image.png', 'ppt/media/image2.png', 'ppt/media/image3.png'}
    changes = []
    with zipfile.ZipFile(path) as original:
        before = {name: original.read(name) for name in original.namelist()}
        after = dict(before)
        for name in sorted(targets):
            data = before[name]
            assert data[:8] == b'\x89PNG\r\n\x1a\n' and data[24] == 16, name
            with Image.open(BytesIO(data)) as im:
                assert im.size == (1920, 1080), (name, im.size)
                icc = im.info.get('icc_profile')
                if not icc:
                    raise ValueError('Expected the original template ICC profile: ' + name)
                srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB'))
                converted = ImageCms.profileToProfile(
                    im, ImageCms.ImageCmsProfile(BytesIO(icc)), srgb, outputMode='RGBA')
                output = BytesIO()
                converted.save(output, format='PNG', icc_profile=srgb.tobytes(), optimize=True)
                new = output.getvalue()
                assert new[24] == 8 and new[25] == 6, name
                after[name] = new
                changes.append({'asset': name, 'size': list(im.size),
                                'before_bit_depth': 16, 'after_bit_depth': 8,
                                'before_sha256': hashlib.sha256(data).hexdigest(),
                                'after_sha256': hashlib.sha256(new).hexdigest()})
        other_media = [name for name in before if name.startswith('ppt/media/') and name not in targets]
        assert len(other_media) == 19
        assert all(before[name] == after[name] for name in other_media)
        fd, temp = tempfile.mkstemp(prefix='phast-portable-media-', suffix='.pptx', dir=path.parent)
        os.close(fd)
        with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as revised:
            for member in original.infolist():
                revised.writestr(member, after[member.filename])
    os.replace(temp, path)
    report = {'scope': 'PNG encoding of overridden template backgrounds only',
              'colour_profile': 'sRGB', 'changed_backgrounds': changes,
              'visible_scientific_images_byte_identical': len(other_media)}
    (path.parent / 'template-media-normalisation.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    normalise(sys.argv[1])
