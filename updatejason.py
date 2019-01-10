import json
import os
from skimage.io import imread
import requests
import csv
path_list=[]
#Write the path to csv
with open("/home/jatin/polyrnn/test.csv",'r') as f:
     reader = csv.reader(f)
     path_list = list(reader)
     
#print(path_list)
def exists(path):
    r = requests.head(path,verify=False)
    return r.status_code == requests.codes.ok
def path_for_url(path):
    for step,i in enumerate(path_list):   
        if path in i:
            #Write the path to folder of images in your system"
            url = "/home/jatin/polyrnn/bhoomi/Bhoomi/"+str(step+1)+".jpg"
            return url
    return "none"
updated=[]

def areas(vertices):
    n = len(vertices) # of corners
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += abs(vertices[i][0] * vertices[j][1]-vertices[j][0] * vertices[i][1])
    result = a / 2.0
    return result

def make_bbox(poly):
    minx = 999999999
    maxx = -1
    miny = 999999999
    maxy = -1
    for point in poly:
        if(point[0]>maxx):
            maxx = point[0]
        if(point[0]<minx):
            minx = point[0]
        if(point[1]>maxy):
            maxy = point[1]
        if(point[1]<miny):
            miny = point[1]
    width = maxx-minx+1
    height = maxy-miny+1
    bbox = [minx,miny,width,height]
    return bbox


def give_width_height(url):
    image = imread(url,plugin='matplotlib')
    return [image.shape[1],image.shape[0]]

def update(filepath,name):
    file = open(filepath,"r")
    data = json.load(file)
    file.close
    data = data["_via_img_metadata"]
    keys = data.keys()
    keys_list = [k for k in keys]
    idx = 0
    key = 0
    for k in keys_list:
        instances = []
        if(k in updated):
            key = 1
            continue
        else:
            key = 0
        tmp = data[k]
        tmp["image_url"] = tmp["filename"]
        path = path_for_url(tmp["image_url"])
        if path!='none':
            tmp["image_url"] = path
        else:
            print("doesnot exist")
            print(tmp["image_url"])
            print("\n")
            updated.append(k)
            continue
        regions = tmp["regions"]
        print(tmp["image_url"])
        count=0
        #if(exists(tmp["image_url"])==False):
         #   print("doesnot exist")
          #  print("\n")
           # updated.append(k)
            #continue
            
        if(len(regions)==0):
            continue
        else:
            updated.append(k)        
        widthheight = give_width_height(tmp["image_url"])
        for r in regions:
            if(r==None):
                continue
            count+=1
            dict = {}
            x_cor = []
            y_cor = []
            area = 0.0
            poly =[]
            r_keys = [k for k in r.keys()]
            if("shape_attributes" not in r_keys):
                continue
            shape_attributes = r["shape_attributes"]
            attributes = [x for x in shape_attributes.keys()]
            if("all_points_x" in attributes):
                x_cor = shape_attributes["all_points_x"]
                y_cor = shape_attributes["all_points_y"]
            else:
                x_cor = [shape_attributes["x"],shape_attributes["x"],shape_attributes["x"]+shape_attributes["width"],shape_attributes["x"]+shape_attributes["width"]]
                y_cor = [shape_attributes["y"],shape_attributes["y"]+shape_attributes["height"],shape_attributes["y"],shape_attributes["y"]+shape_attributes["height"]]
            poly = []
            for x,y in zip(x_cor,y_cor):
                poly.append([x,y])
            if("region_attributes" not in r_keys):
                continue
            region_attributes = r["region_attributes"]
            if "Spatial Annotation" not in region_attributes.keys():
                continue
            label = region_attributes["Spatial Annotation"]
            bbox = make_bbox(poly)
            area = areas(poly)
            components = [{"bbox":bbox,"poly":poly,"area": area}]
            image_width = widthheight[0]
            image_height = widthheight[1]
            image_id = k
            instance_id = k + "_"+ str(count)
            dict = {"image_url":tmp["image_url"],
                    "label" : label,
                    "img_widht" : image_width,
                    "img_height" : image_height,
                    "instance_id" : instance_id,
                    "image_id" : image_id,
                    "bbox" : bbox,
                    "components" : components,
                    "split":"train",
                    }
            instances.append(dict)
        if(key==0 and len(regions)!=0):
            #Write the path where you have to save those json
            outfile = "/home/jatin/polyrnn/data/train/images/" + name[:-5] + str(idx)+".json"
            idx+=1
            with open(outfile,'w') as outfile:
                json.dump(instances,outfile,indent=4)
    
    
#write the path where annotation files are present
mypath = "/home/jatin/polyrnn/jsonfiles"

for (dirpath, dirnames, filenames) in os.walk(mypath):
    for f in filenames:
        update(dirpath+"/"+f,f)


