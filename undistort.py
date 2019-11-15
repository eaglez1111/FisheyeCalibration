import cv2
assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'
import numpy as np
import os
import glob
import sys


#cam1
DIM=(640, 720)
K=np.array([[189.04837356763042, 0.0, 320.33502818808], [0.0, 188.8631149519064, 319.6692104955649], [0.0, 0.0, 1.0]])
D=np.array([[-0.021572964417454973], [0.022703454815758625], [-0.008609733857852585], [-3.083770851860034e-05]])
#cam0
DIM=(640, 720)
K=np.array([[189.35144213743064, 0.0, 318.7193226367838], [0.0, 189.1284221861564, 319.25318522358043], [0.0, 0.0, 1.0]])
D=np.array([[-0.021861138221507193], [0.01950529971822085], [-0.006667800976049638], [-0.00031347154943474917]])

cnt = 0
def undistort_(img_path):
    global cnt
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    if cv2.waitKey(0)& 0xFF == ord('q'):
        quit()
    cv2.destroyAllWindows()


def undistort(img_path, balance=0.0, dim2=None, dim3=None):
    global cnt
    img = cv2.imread(img_path)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    #cv2.imshow("undistorted", undistorted_img)
    cv2.imwrite("/home/liquid/proj/pg/"+str(cnt)+".png", undistorted_img)
    cnt+=1

    #if cv2.waitKey(0)& 0xFF == ord('q'):
    #    quit()
    #cv2.destroyAllWindows()

if __name__ == '__main__':
    #for p in sys.argv[1:]:
    #    undistort(p)
    images = glob.glob(sys.argv[1]+'*.png')

    for fname in images:
        #undistort_(fname)
        undistort(fname,1)
