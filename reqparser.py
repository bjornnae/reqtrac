import uuid
import re
import sys
import json

global current_id
current_id = "0"

global requirements_list
requirements_list = []

global parent_stack
parent_stack = [["MAIN"],[],[],[],[]]

def push_parent_to_stack(level, id):
    global parent_stack
    parent_stack[level].append(id)

def get_parent_from_stack(level):
    global parent_stack
    return (parent_stack[level][-1])

def findindentlevel(line):
    m = re.search("(-+)", line)
    if m:
        return(len(m.group(0)))
    return(1)

def handle_uuid_line(line):
    global current_id
    current_id = line[5:]

def handle_req_line(line):
    global current_id
    if current_id == "0":
        current_id = uuid.uuid4() 
    my_level = findindentlevel(line)
    push_parent_to_stack(my_level, str(current_id))
    parent_id = get_parent_from_stack(my_level - 1)
    requirements_list.append({"parent_id":str(parent_id),  "level" : my_level, "text": line, "id": str(current_id)})  
    current_id = "0"

def handle_other_line(line):
    pass

def dispatch_on_line_type(line):
    if re.search("\Auuid=", line):
        handle_uuid_line(line)
    elif re.search("(-+)", line):
        handle_req_line(line)
    else:
        handle_other_line(line)

def serialize_req_list(requirements_list):
    outstr = ""
    for req in requirements_list:
        outstr += "uuid=%s\n" % str(req["id"])
        outstr += req["text"]
    return outstr

if __name__ == "__main__":
    filename = sys.argv[1]
    lines = []
    with open(filename) as fh:
        lines = fh.readlines()
    for l in lines:
        dispatch_on_line_type(l)
    with open(filename + ".json", "w") as fh2:
        json.dump(requirements_list, fh2 )
    print(serialize_req_list(requirements_list))
