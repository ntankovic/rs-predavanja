"""Download an HTTPS image into project assets without overwriting files."""
import argparse
from pathlib import Path
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 25 * 1024 * 1024


def https_url(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Use an HTTPS URL without embedded credentials.')
    return url


class HTTPSRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        https_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def image_kind(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return '.png'
    if data.startswith(b'\xff\xd8\xff'):
        return '.jpg'
    if data.startswith((b'GIF87a', b'GIF89a')):
        return '.gif'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return '.webp'
    try:
        if ET.fromstring(data).tag == '{http://www.w3.org/2000/svg}svg':
            return '.svg'
    except ET.ParseError:
        pass
    raise ValueError('Response is not a supported image (PNG, JPEG, GIF, WebP, or SVG).')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url', help='Direct HTTPS image URL, not a web page')
    parser.add_argument('destination', help='Path under assets/ or lectures/<lecture>/assets/')
    args = parser.parse_args()
    try:
        https_url(args.url)
        destination = (ROOT / args.destination).resolve()
        relative = destination.relative_to(ROOT)
        parts = relative.parts
        allowed = (len(parts) >= 2 and parts[0] == 'assets') or (
            len(parts) >= 4 and parts[0] == 'lectures' and parts[2] == 'assets')
        if not allowed:
            raise ValueError('Destination must be inside a project assets directory.')
        if destination.exists():
            raise ValueError(f'Destination already exists: {relative}; choose a new filename.')
        suffix = destination.suffix.lower()
        if suffix not in {'.svg', '.png', '.jpg', '.jpeg', '.gif', '.webp'}:
            raise ValueError('Destination must have a supported image extension.')
        opener = urllib.request.build_opener(HTTPSRedirect())
        request = urllib.request.Request(args.url, headers={'User-Agent': 'CourseAssetDownloader/1.0'})
        with opener.open(request, timeout=30) as response:
            https_url(response.url)
            data = response.read(LIMIT + 1)
        if len(data) > LIMIT:
            raise ValueError('Image exceeds the 25 MiB limit.')
        kind = image_kind(data)
        if ('.jpg' if suffix == '.jpeg' else suffix) != kind:
            raise ValueError(f'Image format is {kind}, but destination ends in {suffix}.')
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as target:
            target.write(data)
        print(f'Downloaded {relative} ({len(data):,} bytes)')
    except (ValueError, OSError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
