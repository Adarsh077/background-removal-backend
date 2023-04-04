from pdf2image import convert_from_path


def procress_pdf(file):
    images = convert_from_path('files/' + file.filename)

    saved_images = []

    for i in range(len(images)):
        save_path = 'files/' + file.filename + ' - ' + str(i) + '.jpg'
        images[i].save(save_path, 'JPEG')
        saved_images.append(save_path)

    return saved_images
