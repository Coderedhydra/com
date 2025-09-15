import os
import random
import copy
from backend.class_def import panel


template_specs = {
    "1" : {
        "span" : 1,
        "direction": "row"
    },
    "2" : {
        "span" : 2,
        "direction": "row"
    },
    "3" : {
        "span" : 1,
        "direction": "column"
    },
     "4" : {
        "span" : 2,
        "direction": "column"
    }
      
}

input = '433343333343343333443333443334333343344443433'



def hammingDist(str1, str2): 
    i = 0
    count = 0
  
    while(i < len(str1)): 
        if(str1[i] != str2[i]): 
            count += 1
        i += 1
    return count

def get_files_in_folder(folder_path):
    file_dicts = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            rank = random.randint(1, 3) 

            file_dicts.append({"name": file , 'rank' :  rank})
    return file_dicts

templates = ['1111', '1122', '2211', '1212', '2121']

min_length = 4
folder_path = 'frames/final' # Specify the folder path



def get_templates(input):
    page_templates = []
    start = 0

    while(start<len(input)):
        # print(f"start: {start}")
        result = []
        print(input)
        for template in templates:

            temp = input[start:start + len(template)]
            print(f"start: {start} len:{len(template)} temp:{temp}" )
            result.append(hammingDist(temp,template))            

       
        page_templates.append(templates[result.index(min(result))])

        start = start + len(templates[result.index(min(result))]) 



    if(len(temp) < min_length):
        if(len(temp) ==1):
          temp="5"
        elif(len(temp) ==2):
          temp="67"
        elif(len(temp) ==3):
          temp="666"
        elif(len(temp) ==4):
          temp="4488"
        elif(len(temp) ==5):
          temp="44446"

        page_templates[len(page_templates)-1] = temp
        # print("****************")

    return page_templates


def last_page(panels, count_images, length):
    count = 1
    
    # Handle different remaining panel counts for 2x2 grid
    if length == 1:
        new_panel = panel(f'frame{count_images:03d}', 1, 1)
        panels.append(new_panel)
        # Add panels with next available frames to complete the 2x2 grid
        for i in range(3):
            panels.append(panel(f'frame{count_images + i + 1:03d}', 1, 1))
    elif length == 2:
        for i in range(2):
            new_panel = panel(f'frame{count_images + i:03d}', 1, 1)
            panels.append(new_panel)
        # Add panels with next available frames to complete the 2x2 grid
        for i in range(2):
            panels.append(panel(f'frame{count_images + i + 2:03d}', 1, 1))
    elif length == 3:
        for i in range(3):
            new_panel = panel(f'frame{count_images + i:03d}', 1, 1)
            panels.append(new_panel)
        # Add one panel with next available frame to complete the 2x2 grid
        panels.append(panel(f'frame{count_images + 3:03d}', 1, 1))

    return panels



def panel_create(page_templates):

    panels = []

    images = get_files_in_folder(folder_path)
    print(images)
    
    # Get list of actual frame files
    frame_files = []
    for image in images:
        if image['name'].startswith('frame') and image['name'].endswith('.png'):
            frame_files.append(image['name'])
    
    frame_files.sort()  # Sort to ensure proper order
    print(f"Available frames: {len(frame_files)}")
    
    frame_index = 0

    for page_template in page_templates:

        if(len(page_template)<min_length): #To handle last page 
            panels = last_page(panels, frame_index, len(page_template))
            break

        count = 1
        
        for i in page_template:
            # Use actual available frame files
            if frame_index < len(frame_files):
                frame_name = frame_files[frame_index].replace('.png', '')  # Remove .png extension
                new = panel(frame_name, 1, 1)
                panels.append(new)
                frame_index += 1
            else:
                # Use cycling frame numbers if we run out of actual frames
                cycle_frame = (frame_index % len(frame_files)) if frame_files else 0
                frame_name = f'frame{frame_index + 1:03d}'
                new = panel(frame_name, 1, 1)
                panels.append(new)
                frame_index += 1
            count = count+1

        
    
    return(panels)


# v = get_templates(input)
# print(v)
# new = panel_create(v)


# for i in new:
#     print(i.__dict__)