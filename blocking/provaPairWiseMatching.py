# import Levenshtein
# import os
# import json

# def cluster_creator(elements, distance_value): # distance = distanza di Leveinsthein
#     clusters = {} # Dizionazio: key=cluster_names, value=list_of_elements
    
#     for elem in elements:
#         cluster_match = None
        
#         for cluster_name, cluster_values in clusters.items():
#             for value in cluster_values:
                
#                 distance = Levenshtein.distance(elem, value)
                
#                 if distance <= distance_value: # Se la stringa è simile abbiamo un match
#                     cluster_match = cluster_name 
#                     break
            
#             if cluster_match:   # Se la stringa non è simile, lascia cluster_match = None 
#                 break
        
#         if cluster_match:
#             clusters[cluster_match].append(elem) # Se la stringa è simile aggiungila al cluster trovato
        
#         else:
#             clusters[elem] = [elem]
        
#     return clusters # Ritornami l'intero dizionario

# i = 0

# for i in range (2):
#     json_file_path = os.path.join('sources-json', 'MarScoToc-wikipedia.org.json') # Prova

#     with open(json_file_path, 'r') as json_file:
#         data = json.load(json_file)
        
#     elements = [element.get("Name", "") for element in data]
    

#     distance = 2

#     result_cluster = cluster_creator(elements, distance)

#     # Salvo il cluster in un file .txt

# output = 'clusters.txt'

# with open(output, 'w') as output_file:
#     for cluster_name, cluster_values in result_cluster.items():
#         output_file.write(f"Cluster: {cluster_name}, Values: {cluster_values}\n")
        
# print(f"Clusters saved to {output}")    



# # Extract the value of the "Name" attribute
# elements = [element.get("Name", "") for element in data]


