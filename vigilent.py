import cv2
import base64
from urllib.parse import urlencode
from urllib.request import Request, urlopen

def sendtoserver(img):
    
    server_ip = 'http://192.168.100.1:8000'
    url = f'{server_ip}/v1/api/requester_action'
    #img = cv2.imread(image_file)
    img_b64 = base64.b64encode(img)
    data = {'image': img_b64, 'shape': img.shape}
    data = urlencode(data).encode("utf-8")
    req = Request(url, data)
    response = urlopen(req)
    print(response.read().decode('utf-8'))
    
def main(source='0'):
    
    video_path = source
    
    if video_path.isnumeric() :
        cap = cv2.VideoCapture(int(video_path))
    
    else :
        cap = cv2.VideoCapture(video_path)
    
    if (cap.isOpened() == False):
        print('Error while trying to read video. Please check path again')

    
    while True:
        ret, img = cap.read()
        if not ret:
            print("Cannot receive frame")

            #input()
            continue
        else:
            img = cv2.resize(img,(520,300))               # 縮小尺寸，加快演算速度
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 轉換成 RGB
            break


    #--------------------------------
    #count no of frames
    frame_count = 0
    #count total fps

    #loop until cap opened or video not complete
    while(cap.isOpened):
        
        print("Frame {} Processing".format(frame_count))
        
        #get frame and success from video capture
        ret, frame = cap.read()
        #if success is true, means frame exist
        if ret:
            
            #store frame
            orig_image = frame

            #convert frame to RGB
            image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)

            sendtoserver(image)

if __name__ == "__main__":
    main()