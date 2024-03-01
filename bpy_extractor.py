import bpy
import numpy as np
import json

verticeGroups = {}


PtsLabels = []
edges = []
verticesV=[]
faces_edges = []
edge_nb = []
edge2key = {}
edges_count = 0
nb_count = []
edgeLabels = []


filename =  bpy.context.active_object.name



global_path = '/home/kareem/Desktop/deep_learning/nlp/medical_nlp/intraoral_3d_scanner/'



json_path = global_path+filename+'.json'

ob = bpy.context.object
obdata = bpy.context.object.data

vgroup_names = {vgroup.index: vgroup.name for vgroup in ob.vertex_groups}
vgroups = {v.index: [vgroup_names[g.group] for g in v.groups] for v in obdata.vertices}


#! Getting vertices labels starts here

for v in obdata.vertices:
    coordinate=[v.co.x ,v.co.y, v.co.z]
    verticesV.append(coordinate)
#get group for vertices; save in dict

for idx in range(len(obdata.vertices)):
  
    group = vgroups[idx]
    verticeGroups[idx] = group
    
    if len(group) == 2:
        
         PtsLabels.append(int(group[1]))
    else:
          PtsLabels.append(int(group[0]))
         

# get group of first vertice

# np.savetxt(seg_path.format(bpy.context.active_object.name), PtsLabels, delimiter=',',fmt='%s')

                        ## Getting vertices labels ends here

                        ## Getting FACE labels starts here

face_labels = []
for face in obdata.polygons:
     vert = [face.vertices[0],face.vertices[1],face.vertices[2]]
     most_occurence = np.array([int(vgroups[face.vertices[0]][-1])
                    ,int(vgroups[face.vertices[1]][-1])
                    ,int(vgroups[face.vertices[2]][-1])])
                    
     most_occurence = np.bincount(most_occurence).argmax()
     label = int(most_occurence)
     face_labels.append(label)

                        ## Getting FACE labels ends here

    
     for i in range(3):
           cur_edge = (vert[i], vert[(i + 1) % 3])
           faces_edges.append(cur_edge)

                        ## Getting EDGES labels starts here

for idx, edge in enumerate(faces_edges):
    edge = tuple(sorted(list(edge)))
    faces_edges[idx] = edge
    if edge not in edge2key:
           edge2key[edge] = edges_count
           edges.append(list(edge))




#each edge made of two vertices; get group of first vertice
for idx, edge in enumerate(edges):
      vertix = edge[1]
      groups = verticeGroups[vertix]
      if len(groups) == 2:
         edgeLabels.append(int(groups[1]))
      else:
         edgeLabels.append(int(groups[0]))

                        ## Getting EDGES labels ends here

                        ## saving result as json file

res = {"face_labels":face_labels,"edge_labels":edgeLabels,"vertices_labels":PtsLabels}
with open(json_path,'w+') as fp:
    json.dump(res, fp,  indent=4)



print("Mission Completed",json_path)