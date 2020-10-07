from database import Database
import json
import time


#importing the test data
build_file = open('data/graph_build.json')
build = json.load(build_file)
edit_file = open('data/graph_edits.json')
edits = json.load(edit_file)
img_extract_file = open('data/img_extract.json')
extract = json.load(img_extract_file)
expected_file = open('data/expected_status.json')
expected = json.load(expected_file)

#Run the example

start = time.time()
status = {}
if len(build) > 0:
    # Build graph
    db = Database(build[0][0])
    if len(build) > 1:
    	db.add_nodes(build[1:])
    # Add extract
    db.add_extract(extract)
    # Graph edits
    db.add_nodes(edits)
    # Update status
    status = db.get_extract_status()
end= time.time()
print('Graph updated in %f s'%(end-start))
print(status)
print("Is the result correct",expected==status)