import cv2
import csv
import sys


SCALE_FACTOR = 1/8

nodes_rect = []
draw = False

image_name = 'sample_image.jpg'
image_org = cv2.resize(cv2.imread('data/{}'.format(image_name)),
                       dsize=(0, 0), fx=SCALE_FACTOR, fy=SCALE_FACTOR)

image = image_org.copy()
image_temp = image_org.copy()
image_previous = image_org.copy()
cv2.namedWindow(image_name)
cv2.moveWindow(50, 100)


def label_node(event, x, y, flags, param):
    global nodes_rect, draw, image, image_temp, image_previous
    image_temp = image.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        nodes_rect.append((x-1, y-1))
        draw = True
    elif event == cv2.EVENT_LBUTTONUP:
        nodes_rect.append((x, y))
        cv2.rectangle(
            image_temp, nodes_rect[-2], nodes_rect[-1], (0, 255, 0), -1)
        cv2.imshow("top view", image_temp)
        draw = False
        image_previous = image.copy()
        image = image_temp.copy()
    elif draw:
        cv2.rectangle(image_temp, nodes_rect[-1], (x, y), (0, 255, 0), -1)
        cv2.imshow("top view", image_temp)


# node labeling
cv2.setMouseCallback("top view", label_node)
while True:
    cv2.imshow("top view", image_temp)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("r"):
        image = image_org.copy()
        image_temp = image_org.copy()
        nodes_rect = []
    elif key == ord("u"):
        image = image_previous.copy()
        image_temp = image_previous.copy()
        cv2.imshow("top view", image_temp)
        del nodes_rect[-2:]
    elif key == ord("q"):
        break

# find center of node and compile the data for csv file
nodes = []
for node_id, i in enumerate(range(0, len(nodes_rect), 2)):
    print(nodes_rect[i], nodes_rect[i+1])
    x1, y1 = nodes_rect[i]
    x2, y2 = nodes_rect[i+1]
    node_x = min(x1, x2) + abs(x1-x2)//2
    node_y = min(y1, y2) + abs(y1-y2)//2
    nodes.append([node_id, (node_x, node_y),
                  nodes_rect[i], nodes_rect[i+1]])
    print(nodes[node_id][1], node_id)

# save top-view with nodes marked on it
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
for i in range(len(nodes)):
    cv2.circle(image_org, nodes[i][1], 2, (0, 255, 0), -1)
    cv2.putText(image_org, str(
        nodes[i][0]), nodes[i][1], font, font_scale, (0, 0, 255), 2)
cv2.imwrite('data/image_labeled.png', image_org)
cv2.imshow('image_with node', image_org)
cv2.waitKey(0)

# write node data to csv file
filename = "data/node_data.csv"
fields = ['nodeNumber', 'nodeCenter', 'nodeRectC1', 'nodeRectC2']
with open(filename, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)
    writer.writerows(nodes)

cv2.destroyAllWindows()
