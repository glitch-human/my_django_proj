from django.shortcuts import render, redirect
from .models import MediaFile
from .forms import MediaFileForm

# Create your views here.


def media(request):
    form = MediaFileForm()
    return render(request, 'mediaap/upload.html', {'form': form, })
def upload_file(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_file')
    else:
        form = MediaFileForm()
    media_files = MediaFile.objects.all()
    return render(request, 'mediaap/upload.html',
                  {'form': form, 'media_files': media_files})