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
    if not dim2:
        dim2 = DIM
    if not dim3:
        dim3 = dim2
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, dim2, np.eye(3), balance=balance)
    Knew = cv2.omnidir.Matx33f((640*1.5)/3.1415, 0, 0,0, 640/3.1415, 0, 0, 0, 1);

    print new_K,Knew
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), Knew, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imwrite("/home/liquid/proj/pg/"+str(cnt)+".png", undistorted_img)
    cnt+=1

    cv2.namedWindow('undistorted',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('undistorted', 640,720)
    cv2.imshow("undistorted", undistorted_img)

    if cv2.waitKey(0)& 0xFF == ord('q'):
        quit()
    cv2.destroyAllWindows()

def undistort_j(img_path):
    cam_matrix = np.array([[2.2342347071015597e+03, -3.2044325347697606e+00, 9.4751159627783716e+02], [0,                      2.2237834913412348e+03, 6.4710313963943236e+02],  [0,                      0,                                          1]])
    dist_coefs = np.array([-3.9194270831617489e-01, 1.2746418822062929e-02, -1.3740618480258631e-03, 5.3496926592307157e-03])
    xi = np.array([2.1688260313506302])

    '''the undistortion is performed in this way'''
    img_width = 1920
    img_height = 1208
    Knew = K.copy()
    Knew[0][0] = img_width/2
    Knew[1][1] = img_width/2

    mapx, mapy = cv2.omnidir.initUndistortRectifyMap(K, D, np.array([1.1]), None, Knew,DIM, cv2.CV_32FC1, cv2.omnidir.RECTIFY_PERSPECTIVE)
    img = cv2.imread(img_path)
    img_new = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)

    cv2.imshow("undistorted", img_new)
    cv2.imwrite("test_fixed.png", img_new)
    cv2.waitKey(0)


if __name__ == '__main__':
    #for p in sys.argv[1:]:
    #    undistort(p)
    images = glob.glob(sys.argv[1]+'*.png')

    for fname in images:
        undistort_j(fname)
        undistort(fname,1.0,(640*2,720*2))
        #undistort(fname,1.0)
