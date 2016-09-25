#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pprint,re 
from string import Template
from random import randint

BIKE_HTML = """<script src="https://code.jquery.com/jquery-2.2.4.min.js"   
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
"""

HEADER_HTML = """<div class="row">
    <h3 class="page-header text-left" style="margin-top:0px;">$name</h3>
</div>"""

FEATURES_HTML="""<div class="col-xs-6 col-sm-4">
    <ul>$entries</ul>
</div>
"""

DETAILS_HTML = """<div class="row">
    $list
</div>
<p>$starterPrice</br>$price</p>
"""

FURTHER_BIKE_HTML = """<div class="col-sm-3 col-xs-6">
    <a href="#bikes/$link">
        <img class="img-responsive portfolio-item" src="/bikes$thumbFolder/thumb.jpg" alt="http://placehold.it/500x300">
    </a>
</div>"""

PORTFOLIO_ITEM_HTML = """<div class="col-md-3 portfolio-item">
    <a class="bike" href="#bikes/$link" >
        <img class="img-responsive" src="/bikes$thumbFolder/thumb.jpg" alt="http://placehold.it/750x450">
    </a>
    <h4>$name</h4>
</div>
"""

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
    featuresHtml = "".join([Template(FEATURES_HTML).substitute(entries="".join(chunk)) for chunk in featureChunks])
    detailsHtml = Template(DETAILS_HTML).substitute(list=featuresHtml,starterPrice=starterPrice,price=price)
    #print(detailsHtml)
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
    folder = "/bikes"+bike[1:]
    imagesHtml = "\n\t\t\t\t\t\t".join(["<img src="+str(os.path.join(folder,imageFile))[1:].replace("\\","/")+">" for imageFile in sortImages(imageFiles)])
    #print(imagesHtml)
    return imagesHtml
    
def generateHeader(txtFiles):
    if not txtFiles: return ""
    headerHtml = Template(HEADER_HTML).substitute(name=txtFiles[0].replace(".txt","").encode('ascii', 'xmlcharrefreplace').decode('UTF-8'))
    #print(headerHtml)
    return headerHtml

def generateFurtherBikes(bikeNames):
    furtherBikesHtml = []
    for index in range(4):
        bikeName = bikeNames[randint(0,len(bikeNames)-1)]
        furtherBikeHtml = Template(FURTHER_BIKE_HTML).substitute(thumbFolder=bikeName.replace("\\","/")[1:],link=bikeName.split("\\")[-1])
        furtherBikesHtml.append(furtherBikeHtml)
    #print("".join(furtherBikesHtml))
    return "".join(furtherBikesHtml)

def generateBike(filesPerBike):
    txtFiles = list(filter(lambda f: f.endswith('.txt'),filesPerBike[bike]))
    imageFiles = list(filter(lambda f: f.endswith(".jpg") or f.endswith(".png"),filesPerBike[bike]))
        
    header = generateHeader(txtFiles)
    galery = generateGalery(imageFiles)
    details = generateDetails(txtFiles)
    furtherBikes = generateFurtherBikes(bikes)

    bikeHtml = Template(BIKE_HTML).substitute(header=header,images=galery,details=details,furtherBikes=furtherBikes)
    #print(bikeHtml)
    return bikeHtml


def generateProtfolioItems(filesPerBike):
    items = ['<div class="row">\n']
    for bike in filesPerBike.keys():
        txtFiles = list(filter(lambda f: f.endswith('.txt'),filesPerBike[bike]))
        if not txtFiles: return ""
        txtFile = txtFiles[0]
        item = Template(PORTFOLIO_ITEM_HTML).substitute(
            name=txtFile.replace(".txt",""),
            thumbFolder=bike.replace("\\","/")[1:],
            link=bike.split("\\")[-1]
        )
        bikes = list(filesPerBike.keys())
        index = bikes.index(bike)
        if index % 4 == 0 and index !=0 and index!=len(bikes)-1:
            items.append('</div>\n<div class="row">')
        items.append(item)
    items.append('</div>')
    print("".join(items))
    return "".join(items)

if __name__=="__main__":
    content = [x for x in os.walk('./content')]
    bikes = [x[0] for x in content][1:]
    files = [x[2] for x in content][1:]
    filesPerBike = dict(zip(bikes, files))
    with open("bikes.html", "w") as bikeHtmlFile: 
            bikeHtmlFile.write(generateProtfolioItems(filesPerBike))
    for bike in filesPerBike.keys():
        with open(str(bike.split("\\")[-1])+".html", "w") as bikesHtmlFile: 
            bikesHtmlFile.write(generateBike(filesPerBike))


