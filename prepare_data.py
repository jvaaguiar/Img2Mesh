import os
import glob
import numpy as np
from random import sample
from tools.tools_3d import obj_normals
from tools.obj_tools import read_obj

# ==============================================================================
# fetch .npy data (X: 6 images) (Y: vertices positions)
#
# fetch_faces == True = (faces: list of vertices for each face)
def fetchData (path, lean=True, fetch_faces=False):
    X = []
    Y = []
    faces = []

    files = glob.glob(os.path.join(path, '*.npy'))
    for file in files:
        data = np.load(file, allow_pickle=True).item()
        
        if (lean == True):
            X.append([data['left']])
        else:
            X.append([
                data['top'],    data['bottom'],
                data['front'],  data['back'],
                data['left'],   data['right']])

        Y.append(np.array(data['vertices'], dtype='float32'))
        if (fetch_faces == True):
            faces.append(np.array(data['faces'], dtype='int32'))
    
    if (fetch_faces == True):
        return X, Y, faces
    return X, Y

# ==============================================================================
# returns all data from the .npy files in the path
def prepareData (paths, lean=True, fetch_faces=False):
    X = []
    Y = []
    faces = []
    for p in paths:
        if (fetch_faces == True):
            x_p, y_p, f_p = fetchData(p, lean=lean, fetch_faces=True)
            faces.extend(f_p)
        else:
            x_p, y_p = fetchData(p, lean=lean, fetch_faces=False)
        
        X.extend(x_p)
        Y.extend(y_p)

    if (fetch_faces == True):
        return X, Y, faces
    return X, Y

# ==============================================================================
# create slices for each batch in training
def createBatches (length, batch_size=16):
    batches = []

    offset = 0
    while offset < length - batch_size:
        batches.append(slice(offset, offset+batch_size))
        offset = offset + batch_size
    
    batches.append(slice(offset, None))

    return batches

# ==============================================================================
# reduces the number of vertices in a model
def downsample(data, k=50000, get_normals=False, faces=None):
    out = []    # vertices positions of output
    normals = []# vertex normals of output
    
    if (get_normals == True):
        prev = 0
        i = 0
        print("DONWSAMPLE WITH NORMALS: ", end='')
        for d, f in zip(data, faces):
            i = i + 1
            new = int(10 * i / len(data))
            if (new > prev):
                prev = new
                print('.', end='')

            if len(d) > k:
                idx = np.random.choice(len(d), size=k, replace=False)
                idx, ns = obj_normals(d, f, idx)
                
                out.append(d[idx])
                normals.append(ns)
            else:
                idx, ns = obj_normals(d, f, np.array(range(len(d))))
                
                out.append(d[idx])
                normals.append(ns)
        print()
        return out, normals
    else:    
        for d in data:
            if len(d) > k:
                idx = np.random.choice(len(d), size=k, replace=False)
                out.append(d[idx])
            else:
                out.append(d)
        return out


# ==============================================================================
# prepares a mask of faces wich each vertice is part of
# for normal_loss computing
def prepare_mask(path='./models/ico_162.obj'):
    _, faces = read_obj(path)
    mask = []
    lens = []
    for i in np.unique(faces):
        mask.append(np.where(faces == i)[0])
        lens.append(len(mask[-1]))
    
    max_l = np.max(lens)
    for i in range(len(mask)):
        if (lens[i] < max_l):
            mask[i] = np.pad(mask[i],
                             (0, max_l - lens[i]),
                             constant_values=np.random.choice(mask[i]))
    
    return np.array(faces), np.array(mask)