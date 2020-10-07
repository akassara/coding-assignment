import networkx as nx


class Database(object):
	def __init__(self, name="Core"):

		self.name = name
		self.db_dict = {}
		# We represent the label hierarchy by a directed graph
		self.label_graph = nx.DiGraph()
		# We assign to each node(label) two attributes: the age (old or recent) to see what are the latest nodes
		# and the status(valid or granularity_staged or coverafe_staged or invalid)
		self.label_graph.add_nodes_from([(name, {'age': 'new', "status": "valid"})])
		print("A database object is created.")

	def add_nodes(self, new_nodes):
		# The node already savec are old and valid
		for node in self.label_graph.nodes:
			self.label_graph.nodes[node]['age'] = 'old'
			self.label_graph.nodes[node]['status'] = 'valid'
		# We add the new nodes and we update their status
		for i in range(len(new_nodes)):
			node = new_nodes[i][0]
			parent = new_nodes[i][1]
			# The new nodes are valid
			new_child = (node, {'age': 'new', 'status': 'valid'})
			self.label_graph.add_nodes_from([new_child])
			#We add the edge betwen the node and its parent
			self.label_graph.add_edges_from([(parent, node)])
			# If the parent is old and it hasn't a staged coverage, which has the priority, then as he has a new son we update its granularity
			if self.label_graph.nodes[parent]['age'] == 'old' and self.label_graph.nodes[parent][
				'status'] != 'coverage_staged':
				self.label_graph.nodes[parent]['status'] = 'granularity_staged'
			# bros is the list of brothers(nodes that have a same father)
			bros = list(self.label_graph.successors(parent))
			if len(bros) > 1:
				for bro in bros:
					# if one of the brothers is old, we update its coverage
					if bro != node and self.label_graph.nodes[bro]['age'] == "old":
						self.label_graph.nodes[bro]['status'] = "coverage_staged"

		print("All new nodes have been added")

	def add_extract(self, extract_dict):
		for key in extract_dict.keys():
			# in case an image is already there and has a new label
			if key in self.db_dict.keys():
				self.db_dict[key] = self.db_dict[key] + extract_dict[key]
			else:
				self.db_dict[key] = extract_dict[key]
		print("All new extracts have been added to the database")

	def get_extract_status(self):

		status = self.db_dict
		label_status = {node: self.label_graph.nodes[node]['status'] for node in list(self.label_graph.nodes)}
		for key in status.keys():
			labels = status[key]
			for i in range(len(labels)):
				if labels[i] in label_status.keys():
					if label_status[labels[i]] == "coverage_staged":
						status[key][i] = "coverage_staged"
					elif label_status[labels[i]] == "granularity_staged":
						status[key][i] = "granularity_staged"
					else:
						status[key][i] = "valid"
				else:
					status[key] = "invalid"
					# if there is at least one invalid label, then the image is invalid
					break
			#priority to the coverage_staged
			if "coverage_staged" in status[key]:
				status[key] = "coverage_staged"

			elif "granularity_staged" in status[key] and status[key] != "coverage_staged":
				status[key] = "granularity_staged"

			elif status[key] != "invalid" and status[key] != "coverage_staged":
				status[key] = "valid"

		return status
