import os
import shutil
import fileinput
import time
import fnmatch
from css_html_js_minify import process_single_html_file, process_single_js_file, process_single_css_file, html_minify, js_minify, css_minify


def getListOfFiles(dirName, filenames='', inSub=True, withoutFolders=True):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)

        if os.path.isdir(fullPath) is False and filenames != '':
            if fnmatch.fnmatch(entry, filenames) is False:
                continue

        if os.path.isdir(fullPath) and inSub:
            allFiles = allFiles + getListOfFiles(fullPath, filenames=filenames, inSub=inSub, withoutFolders=withoutFolders)
        else:
            if os.path.isdir(fullPath) and withoutFolders is True:
                continue
            allFiles.append(fullPath)

    return allFiles


def resample(name, files):
    htmlcpp = open(path + "/" + name, 'w+')
    htmlcpp.write('#include <pgmspace.h>\n\n\n')
    htmlcpp.flush()
    htmlcpp.close()
    time.sleep(.2)
    htmlcpp = open(path + "/" + name, mode='a', encoding="utf8")
    for file in files:
        file_name = os.path.basename(file).replace('.', '_')
        htmlcpp.write('char ' + file_name + '[] PROGMEM = R"=====(')
        htmlcpp.write('\n')
        file_f = open(file, mode="r", encoding="utf8")
        for lineinfile in file_f:
            htmlcpp.write(lineinfile)
        file_f.close()
        htmlcpp.write('\n')
        htmlcpp.write(')=====";')
        htmlcpp.write('\n\n')
        htmlcpp.flush()
    htmlcpp.flush()
    htmlcpp.close()


path = "D:/Web/Pek/DeviceWebIn/SmartPatrom"

minPath = path + "/smartpatrom_min"
minJsPath = minPath
minCssPath = minPath
shutil.rmtree(minPath, True)
time.sleep(.2)
os.mkdir(minPath)

time.sleep(.2)

htmlFiles = getListOfFiles(path + "/smartpatrom/", inSub=False)
jsFiles = getListOfFiles(path + "/smartpatrom/js/", inSub=False)
cssFiles = getListOfFiles(path + "/smartpatrom/css/", inSub=False)

for html in htmlFiles:
    html_min = process_single_html_file(html, overwrite=False)
    html_min_name = os.path.basename(html_min).replace(".htmll", ".html")
    shutil.move(html_min, minPath + "/" + html_min_name)

for js in jsFiles:
    js_min = process_single_js_file(js, overwrite=False)
    js_min_name = os.path.basename(js_min).replace(".min", "")
    shutil.move(js_min, minJsPath + "/" + js_min_name)

for css in cssFiles:
    css_min = process_single_css_file(css, overwrite=False)
    css_min_name = os.path.basename(css_min).replace(".min", "")
    shutil.move(css_min, minCssPath + "/" + css_min_name)

time.sleep(.2)

line = ""
for line in fileinput.input(minPath + "/" + "index.html", inplace=False):
    line = line.replace('<link href="css/', '<link href="')
    line = line.replace('<script src="js/', '<script src="')
    print(line)

f = open(minPath + "/" + "index.html", 'w')
f.write(line)
f.close()

time.sleep(.2)

resample('HTML.cpp', getListOfFiles(path + "/smartpatrom/"))
resample('HTML.min.cpp', getListOfFiles(path + "/smartpatrom_min/"))
