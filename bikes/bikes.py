#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pprint,re 
from string import Template
from random import randint

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def generateDetails(txtFiles):
    if not txtFiles: return ""
    txtFile = txtFiles[0]
    bikeName = txtFile.split('.')[0]
    txtContent = [line.rstrip('\n').strip().encode('ascii', 'xmlcharrefreplace').decode('UTF-8') for line in open(os.path.join(bike,txtFile)) if line.strip()]
    starterPrice = txtContent[::-1][1]
    price = txtContent[::-1][0]
    details = txtContent[:-2]
    featureList = ['<li>'+str(detail)+'</li>' for detail in details]
    featureChunks = list(chunks(featureList,3))
    featuresHtml = "".join([Template(
"""             <div class="col-xs-6 col-sm-4">
                <ul>$entries</ul>
            </div>
""").substitute(entries="".join(chunk)) for chunk in featureChunks])
    detailsHtml = Template(
"""<div class="row">
$list
        </div>
        <p>$starterPrice</br>$price</p>
""").substitute(list=featuresHtml,starterPrice=starterPrice,price=price)
    print(detailsHtml)
    return detailsHtml

def sortImages(l): 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    sortedItems = sorted(l, key = alphanum_key)
    thumb = list(filter(lambda t: "thumb" in t  ,sortedItems))
    if not thumb: return sortedItems
    thumb = thumb[0]
    sortedItems.remove(thumb)
    sortedItems.insert(0,thumb)
    return sortedItems

def generateGalery(imageFiles):
    imagesHtml = "\n\t\t\t\t\t\t".join(["<img src="+str(os.path.join(bike,imageFile))[1:].replace("\\","/")+">" for imageFile in sortImages(imageFiles)])
    #print(imagesHtml)
    return imagesHtml
    
def generateHeader(txtFiles):
    if not txtFiles: return ""
    headerHtml = Template(
        """<div class="row">
    <h3 class="page-header text-left" style="margin-top:0px;">$name</h3>
        </div>
        """).substitute(name=txtFiles[0].replace(".txt","").encode('ascii', 'xmlcharrefreplace').decode('UTF-8'))
    #print(headerHtml)
    return headerHtml

def generateFurtherBikes(bikeNames):
    furtherBikesHtml = []
    for index in range(4):
        bikeName = bikeNames[randint(0,len(bikeNames)-1)]
        furtherBikeHtml = Template(
            """<div class="col-sm-3 col-xs-6">
                <a href="#bikes/$link">
                    <img class="img-responsive portfolio-item" src="$thumbFolder/thumb.jpg" alt="http://placehold.it/500x300">
                </a>
            </div> """).substitute(thumbFolder=bikeName.replace("\\","/")[1:],link=bikeName.split("\\")[-1])
        furtherBikesHtml.append(furtherBikeHtml)
    #print("".join(furtherBikesHtml))
    return "".join(furtherBikesHtml)


if __name__=="__main__":
    content = [x for x in os.walk('./content')]
    bikes = [x[0] for x in content][1:]
    files = [x[2] for x in content][1:]
    filesPerBike = dict(zip(bikes, files))
    for bike in filesPerBike.keys():
        txtFiles = list(filter(lambda f: f.endswith('.txt'),filesPerBike[bike]))
        imageFiles = list(filter(lambda f: f.endswith(".jpg") or f.endswith(".png"),filesPerBike[bike]))
        
        header = generateHeader(txtFiles)
        galery = generateGalery(imageFiles)
        details = generateDetails(txtFiles)
        furtherBikes = generateFurtherBikes(bikes)

        bikeHtml = Template(
"""<script src="https://code.jquery.com/jquery-2.2.4.min.js"   
    integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44="   
    crossorigin="anonymous">
</script>
<script src="./index_files/bootstrap.min.js"></script>
<script src="./index_files/galleria-1.4.2.min.js"></script>
$header
<div class="row">
    <div>
        <div id="galleria" class="galleria embed-responsive embed-responsive-16by9">
            $images
        </div>
    </div >
    <div class="text-left">
        <div><h3 class="page-header">Details</h3></div>
        $details
        </div>
        <div>
            <div><h3 class="page-header text-left">Weitere Bikes</h3></div>
            $furtherBikes
        </div>
<script>
    Galleria.loadTheme('./index_files/themes/azur/galleria.azur.min.js');
    Galleria.run('#galleria', {responsive:true,height:0.5625});
</script>
""").substitute(header=header,images=galery,details=details,furtherBikes=furtherBikes)
        print(bikeHtml)
        with open(str(bike.split("\\")[-1])+".html", "w") as bikeHtmlFile: bikeHtmlFile.write(bikeHtml)


