import os
import requests
import zipfile


def listFiles(folder):
    return os.listdir(folder)


def deleteFile(filepath):
    os.remove(filepath)
    return


def deleteFolder(path):
    os.rmdir(path)
    return


def fileExists(filename):
    return os.path.exists(filename)


def cleanFolder(folder):
    files = listFiles(folder)
    for file in files:
        deleteFile('{0}/{1}'.format(folder, file))

    return


def requestUrl(url):
    return requests.get(url)


def downloadFile(url, filename):
    with open(filename, 'wb') as f:
        with requests.get(url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    return


def extractFile(filename, extractpath, autoclean=True):
    try:
        z = zipfile.ZipFile(filename)
        z.extractall(path=extractpath)
    except Exception as ex:
        print('Unable to extract file {0}'.format(filename), str(ex))

    if autoclean:
        os.remove(filename)

    return