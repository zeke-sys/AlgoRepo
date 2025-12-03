import heapq
import cv2
import matplotlib.pyplot as plt

# print ("OpenCV version:", cv2.__version__)
#print(os.getcwd())

# Solving Image Maze given a 2D image
# We view the image as a graph where each pixel is a vertex and edges connect a pixel to its neighbors
# We will use the Djikstra algorithm to find the shortest path from start to end pixel
# It can exit as soon as the destination is reached
# A 1000x1000 pixel image gives rise to a graph with 1 million vertices. Storing such a graph is not feasible
# Instead, we will compute the vertices and edges on the fly as needed during the algorithm
# We will use opencv to read and manipulate the image


# Reading Image with opencv
img = cv2.imread('images/maze.png')  # read image from file using opencv (cv2) library

# annotating images (OpenCV uses BGR color ordering)
# cv2.circle(img, (5,220), 3, (255,0,0), -1)
# cv2.circle(img, (5,5), 3, (0,0,255), -1)
# plt.imshow(img) # show image on screen
# plt.title('Amazing')
# plt.show()

# given an image, read the color at a pixel
# Reading the color at pixel (145, 67)
print("The pixel color is expressed in RGB format. R is the red value from 0->255, ")
print("G is the green value 0->255, and B is the blue value from 0->255.")
print('Image size (height, width, num layers) is', img.shape)
px = img[145, 67] # img[y, x] is the color of the pixel x, y
print(px)

# cv2.circle(img, (80, 18), 3, (198,31,4), -1) # draw colored circle centered at (80, 18)
# px1 = img[18, 80] # It is important to note that rows of the image are y values and columns are x values
# print(px1)

px2 = img[80, 18] # Indexing the img data structure data takes y, x values
print(px2)

# Define edge weight function for an edge in the image
def fixPixelValues(px):
    # convert the RBG valeus into floating point to avoid an overflow that gives the wrong answers
    return [float(px[0]), float(px[1]), float(px[2])]

# given (x, y) coordinates of two neighboring pixels, calculate the edge weight
# we take the squared euclidean distance between the pixel values and add 0.1
def getEdgeWeight(img, u, v):
    # get edge weight for edge between u, v
    # first make sure that the edge is legit
    i0,j0 = u[0], u[1]
    i1,j1 = v[0], v[1]
    height, width, _ = img.shape
    
    # pixel poistion valid?
    assert i0 >= 0 and j0 >= 0 and i0 < width and j0 < height
    assert i1 >= 0 and j1 >= 0 and i1 < width and j1 < height 
    #edge between node and neighbor?
    assert -1 <= i0 - i1 <= 1
    assert -1 <= j0 - j1 <= 1

    px1 = fixPixelValues(img[j0,i0])
    px2 = fixPixelValues(img[j1,i1])
    return 0.1 + (px1[0] - px2[0])**2 + (px1[1] - px2[1])**2 + (px1[2] - px2[2])**2

# given a list of (x, y) values, draw a series of red lines between each coordinate
# and next show the path in the image
def drawPath(img, path, pThick=2):
    if not path:
        return
    v = path[0]
    x0, y0 = v[0], v[1]
    for v in path:
        x, y = v[0], v[1]
        cv2.line(img, (x, y), (x0, y0), (0, 0, 255), pThick)
        x0, y0 = x, y

# computing single source shortest path using Dijkstra's algorithm
# for simplicity, we'll try a first cut implementation that uses a priority queue
class Vertex: # out line for a vertex data structure
    def __init__(self, i, j):
        self.x = i # The x coordinate (row index)
        self.y = j # The y coordinate (column index)
        self.d = float('inf') # the shortest path estimate from source
        self.processed = False # whether this vertex has been processed
        self.idx_in_priority_queue = -1 # index in the priority queue
        self.pi = None # parent vertex in the shortest path tree

# Dijskstra's algorithm requires a priority queue so that the minimum
# weight vertex can be extracted efficiently
class PriorityQueue:
    def __init__(self):
        self.heap = [] # heap array
        self.vertex_map = {} # map from (i, j) to vertex object

    # insert a vertex into the priority queue
    def insert(self, vertex):
        heapq.heappush(self.heap, (vertex.d, id(vertex), vertex)) # push tuple (distance, vertex)
        self.vertex_map[(vertex.x, vertex.y)] = vertex

    # extract the minimum weight vertex
    def get_and_delete_min(self):
        while self.heap:
            _, _, vertex = heapq.heappop(self.heap)
            if not vertex.processed:
                vertex.processed = True
                # remove from map if present
                self.vertex_map.pop((vertex.x, vertex.y), None)
                return vertex
        return None

    def is_empty(self):
        # consider the queue empty when there are no known unprocessed vertices
        return len(self.vertex_map) == 0

    # update the weight
    def update_vertex_weight(self, vertex):
        # since heapq does not support decrease key, we re-insert the vertex
        heapq.heappush(self.heap, (vertex.d, id(vertex), vertex))
        # ensure the vertex is tracked as pending
        self.vertex_map[(vertex.x, vertex.y)] = vertex

# implementing Dijkstra's algorithm to compute shortest path in an image
def computeShortestPath(image, start, dest):
    # treat start and dest as (x, y) coordinates (same ordering as cv2 drawing routines),
    # convert to internal (row, col) = (y, x) representation for processing.
    rows, cols = image.shape[:2]
    vertices = {} # map from (row, col) to vertex object

    def get_vertex(i, j):
        if (i, j) not in vertices: # create new vertex
            vertices[(i, j)] = Vertex(i, j)
        return vertices[(i, j)]
    
    # convert external (x,y) to internal (row, col)
    start_row, start_col = start[1], start[0]
    dest_row, dest_col = dest[1], dest[0]

    start_vertex = get_vertex(start_row, start_col)
    start_vertex.d = 0

    pq = PriorityQueue() # create priority queue
    pq.insert(start_vertex) # insert start vertex

    while not pq.is_empty():
        u = pq.get_and_delete_min() # get vertex with minimum distance
        if u is None:
            break
        if (u.x, u.y) == (dest_row, dest_col): # reached destination (internal coords)
            break

        # explore neighbors (4-connectivity)
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = u.x + di, u.y + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                px = image[ni, nj]
                # compute a scalar intensity robustly for color (BGR) or grayscale images
                mean_func = getattr(px, 'mean', None)
                if callable(mean_func):
                    intensity = float(px.mean())
                else:
                    try:
                        intensity = float(px)
                    except Exception:
                        # fallback for sequences like lists/tuples
                        intensity = float(sum(px) / len(px))

                if intensity < 50: # threshold for walls (dark pixels)
                    continue

                v = get_vertex(ni, nj)
                # uniform cost for traversable pixel (you can replace with color-difference weight if desired)
                weight = 1.0
                if not v.processed and u.d + weight < v.d:
                    v.d = u.d + weight
                    v.pi = u
                    pq.update_vertex_weight(v)

    # reconstruct path and return in external (x, y) ordering for drawPath/cv2 (col, row)
    path = []
    dest_vertex = vertices.get((dest_row, dest_col))
    if dest_vertex is None or dest_vertex.d == float('inf'):
        # unreachable destination
        return []

    current = dest_vertex
    while current is not None:
        # convert internal (row, col) -> external (x=col, y=row)
        path.append((current.y, current.x))
        current = current.pi
    path.reverse()

    return path

p = computeShortestPath(img, (5,220), (5,5))

# Draw first path
drawPath(img, p, 2)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb) # show image without color conversion by OpenCV-Matplotlib
plt.title('Amazing')
plt.show()
cv2.imwrite('maze-solution.png', img)

# Show second image
img = cv2.imread('images/maze2.JPG') # read image
#cv2.circle(img, (250,470), 10, (255,0,0), -1)
#cv2.circle(img, (20,100), 10, (255,0,0), -1)
#plt.imshow(img) #show image
#plt.title('Amazing 2')
#plt.show()

p = computeShortestPath(img, (250,470), (20,100))

# Draw second path
drawPath(img, p)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # show image
plt.title('Amazing2')
plt.show()


