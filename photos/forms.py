from django import forms

class ImageUploadForm(forms.Form):
    file = forms.FileField()

    # def __init__(self, *args, **kwargs):
    #     if request.FILES:
    #         image_uploader = ImageUploader()
    #         for file in request.FILES:
    #             image_uploader.upload_image(file)
