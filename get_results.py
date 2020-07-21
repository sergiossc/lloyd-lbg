import os
import uuid
import json
import matplotlib.pyplot as plt
import numpy as np


def check_files(prefix, episodefiles):
    pathfiles = {}
    for ep_file in episodefiles:
        pathfile = prefix + str('/') + str(ep_file)
        ep_file_status = False
        try:
            current_file = open(pathfile)
            ep_file_status = True
            #print("Sucess.")
        except IOError:
            print("File not accessible: ", pathfile)
        finally:
            current_file.close()

        if ep_file_status:
            ep_file_id = uuid.uuid4()
            pathfiles[ep_file_id] = pathfile
 
    return pathfiles


def decode_mean_distortion(mean_distortion_dict):
    mean_distortion_list = []
    for iteration, mean_distortion in mean_distortion_dict.items():
        mean_distortion_list.append(mean_distortion)
    return mean_distortion_list




prefix_pathfiles = '/home/snow/code/lloyd-toy/results/'
result_files = os.listdir(prefix_pathfiles)

pathfiles = check_files(prefix_pathfiles, result_files)
print ('# of json files: ', len(pathfiles))
 

#fig, ax = plt.subplots()
for pathfile_id, pathfile in pathfiles.items():
    with open(pathfile) as result:
        data = result.read()
        d = json.loads(data)
    num_of_cw = d["num_of_cw"]
    var = d["variance_of_samples"]
    var = float("{:.2f}".format(var))
    sets =  d["sets"]
    mean_distortion = decode_mean_distortion(d["mean_distortion"])
    lloyd_codebook = d["lloydcodebook"]
    
    if num_of_cw == 4:
        if var == 0.5:
            print (sets)
