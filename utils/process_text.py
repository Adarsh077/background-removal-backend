from pdf2image import convert_from_path
import urllib.request


def procress_text(file):
    saved_images = []
    file_path = 'files/' + file.filename
    with open(file_path, 'r') as f:
        image_urls = f.read().split('\n')
        for url in image_urls:
            if url == '':
                continue
            file_name = url.split('/')[-1]
            save_path = 'files/' + file_name
            print(save_path)
            f = open(save_path, 'wb')
            f.write(urllib.request.urlopen(url).read())
            f.close()
            saved_images.append(save_path)

    return saved_images
