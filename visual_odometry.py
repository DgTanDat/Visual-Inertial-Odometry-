# import numpy as np 
# import cv2

# STAGE_FIRST_FRAME = 0
# STAGE_SECOND_FRAME = 1
# STAGE_DEFAULT_FRAME = 2
# kMinNumFeature = 1500

# lk_params = dict(winSize  = (20, 20), 
# 				# maxLevel = 3,
#              	criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

# def featureTracking(image_ref, image_cur, px_ref):
# 	kp2, st, err = cv2.calcOpticalFlowPyrLK(image_ref, image_cur, px_ref, None, **lk_params)  #shape: [k,2] [k,1] [k,1]

# 	st = st.reshape(st.shape[0])
# 	kp1 = px_ref[st == 1]
# 	kp2 = kp2[st == 1]

# 	return kp1, kp2


# class PinholeCamera:
# 	def __init__(self, width, height, fx, fy, cx, cy, 
# 				k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0):
# 		self.width = width
# 		self.height = height
# 		self.fx = fx
# 		self.fy = fy
# 		self.cx = cx
# 		self.cy = cy
# 		self.distortion = (abs(k1) > 0.0000001)
# 		self.d = [k1, k2, p1, p2, k3]
		


# class VisualOdometry:
# 	def __init__(self, cam, annotations):
# 		self.frame_stage = 0
# 		self.cam = cam
# 		self.new_frame = None
# 		self.last_frame = None
# 		self.cur_R = None
# 		self.cur_t = None
# 		self.px_ref = None
# 		self.px_cur = None
# 		self.brief_ref = None
# 		self.brief_cur = None
# 		self.focal = cam.fx
# 		self.pp = (cam.cx, cam.cy)
# 		self.K = np.array([[cam.fx, 0, cam.cx],
# 							[0, cam.fy, cam.cy],
# 							[0, 0, 1]], dtype=np.float32)
# 		self.trueX, self.trueY, self.trueZ = 0, 0, 0
# 		# self.detector = cv2.FastFeatureDetector_create(threshold=25, nonmaxSuppression=True)
# 		self.detector = cv2.ORB_create(3000, scaleFactor=1.3, nlevels=4, fastThreshold=25, scoreType=cv2.ORB_FAST_SCORE) #cv2.ORB_FAST_SCORE
# 		with open(annotations) as f:
# 			self.annotations = f.readlines()

# 	def getAbsoluteScale(self, frame_id):  #specialized for KITTI odometry dataset
# 		ss = self.annotations[frame_id-1].strip().split()
# 		x_prev = float(ss[3])
# 		y_prev = float(ss[7])
# 		z_prev = float(ss[11])
# 		ss = self.annotations[frame_id].strip().split()
# 		x = float(ss[3])
# 		y = float(ss[7])
# 		z = float(ss[11])
# 		self.trueX, self.trueY, self.trueZ = x, y, z
# 		return np.sqrt((x - x_prev)*(x - x_prev) + (y - y_prev)*(y - y_prev) + (z - z_prev)*(z - z_prev))
	
	

# 	def processFirstFrame(self):
# 		# self.px_ref = self.detector.detect(self.new_frame)
# 		self.px_ref, self.brief_ref = self.detector.detectAndCompute(self.new_frame, None)
# 		self.px_ref = np.array([x.pt for x in self.px_ref], dtype=np.float32)
# 		self.frame_stage = STAGE_SECOND_FRAME

# 	def processSecondFrame(self):
# 		self.px_ref, self.px_cur = featureTracking(self.last_frame, self.new_frame, self.px_ref)
# 		# F, mask = cv2.findFundamentalMat(self.px_ref, self.px_cur, method=cv2.RANSAC, ransacReprojThreshold=1.0, confidence=0.99)
        
# 		E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp, method=cv2.RANSAC, prob=0.999, threshold=1.0)
# 		_, self.cur_R, self.cur_t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp = self.pp)
		
# 		# E = self.K.T @ F @ self.K
# 		# _, self.cur_R, self.cur_t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp = self.pp)
# 		self.frame_stage = STAGE_DEFAULT_FRAME 
# 		self.px_ref = self.px_cur

# 	def processFrame(self, frame_id):
# 		self.px_ref, self.px_cur = featureTracking(self.last_frame, self.new_frame, self.px_ref)
# 		E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp, method=cv2.RANSAC, prob=0.999, threshold=1.0)
# 		_, R, t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp = self.pp)
# 		absolute_scale = self.getAbsoluteScale(frame_id)
# 		if(absolute_scale > 0.1):
# 			self.cur_t = self.cur_t + absolute_scale * self.cur_R.dot(t)  # * absolute_scale #self.cur_R.dot(t)
# 			self.cur_R = R.dot(self.cur_R)
# 		# add new keypoints if the number of features is less than kMinNumFeature
# 		if(self.px_ref.shape[0] < kMinNumFeature):
# 			# self.px_cur, self.brief_cur = self.detector.detect(self.new_frame)
# 			self.px_cur, self.brief_cur = self.detector.detectAndCompute(self.new_frame, None)
# 			self.px_cur = np.array([x.pt for x in self.px_cur], dtype=np.float32)
# 		self.px_ref = self.px_cur

# 	def update(self, img, frame_id):
# 		assert(img.ndim==2 and img.shape[0]==self.cam.height and img.shape[1]==self.cam.width), "Frame: provided image has not the same size as the camera model or image is not grayscale"
# 		self.new_frame = img
# 		if(self.frame_stage == STAGE_DEFAULT_FRAME):
# 			self.processFrame(frame_id)
# 		elif(self.frame_stage == STAGE_SECOND_FRAME):
# 			self.processSecondFrame()
# 		elif(self.frame_stage == STAGE_FIRST_FRAME):
# 			self.processFirstFrame()
# 		self.last_frame = self.new_frame





# import numpy as np
# import cv2

# STAGE_FIRST_FRAME = 0
# STAGE_SECOND_FRAME = 1
# STAGE_DEFAULT_FRAME = 2
# kMinNumFeature = 500  # Minimum number of features

# lk_params = dict(winSize=(21, 21),
#                  criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

# def featureTracking(image_ref, image_cur, px_ref):
#     kp2, st, err = cv2.calcOpticalFlowPyrLK(image_ref, image_cur, px_ref, None, **lk_params)  # shape: [k,2] [k,1] [k,1]
#     st = st.reshape(st.shape[0])
#     kp1 = px_ref[st == 1]
#     kp2 = kp2[st == 1]
#     return kp1, kp2

# class PinholeCamera:
#     def __init__(self, width, height, fx, fy, cx, cy,
#                  k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0):
#         self.width = width
#         self.height = height
#         self.fx = fx
#         self.fy = fy
#         self.cx = cx
#         self.cy = cy
#         self.distortion = (abs(k1) > 0.0000001)
#         self.d = [k1, k2, p1, p2, k3]

# class VisualOdometry:
#     def __init__(self, cam, annotations):
#         self.frame_stage = 0
#         self.cam = cam
#         self.new_frame = None
#         self.last_frame = None
#         self.cur_R = None
#         self.cur_t = None
#         self.px_ref = None
#         self.px_cur = None
#         self.focal = cam.fx
#         self.pp = (cam.cx, cam.cy)
#         self.trueX, self.trueY, self.trueZ = 0, 0, 0
#         # Khởi tạo ORB detector thay cho FAST
#         self.detector = cv2.ORB_create(nfeatures=1000, scaleFactor=1.2, nlevels=8, edgeThreshold=31, firstLevel=0,
#                                        WTA_K=2, scoreType=cv2.ORB_HARRIS_SCORE, patchSize=31, fastThreshold=20)
#         with open(annotations) as f:
#             self.annotations = f.readlines()

#     def getAbsoluteScale(self, frame_id):  # specialized for KITTI odometry dataset
#         ss = self.annotations[frame_id-1].strip().split()
#         x_prev = float(ss[3])
#         y_prev = float(ss[7])
#         z_prev = float(ss[11])
#         ss = self.annotations[frame_id].strip().split()
#         x = float(ss[3])
#         y = float(ss[7])
#         z = float(ss[11])
#         self.trueX, self.trueY, self.trueZ = x, y, z
#         return np.sqrt((x - x_prev)**2 + (y - y_prev)**2 + (z - z_prev)**2)

#     def processFirstFrame(self):
#         # Phát hiện keypoints bằng ORB
#         keypoints = self.detector.detect(self.new_frame, None)
#         self.px_ref = np.array([kp.pt for kp in keypoints], dtype=np.float32)
#         self.frame_stage = STAGE_SECOND_FRAME

#     def processSecondFrame(self):
#         self.px_ref, self.px_cur = featureTracking(self.last_frame, self.new_frame, self.px_ref)
#         E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp,
#                                        method=cv2.RANSAC, prob=0.99, threshold=1.0)
#         _, self.cur_R, self.cur_t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref,
#                                                           focal=self.focal, pp=self.pp)
#         self.frame_stage = STAGE_DEFAULT_FRAME
#         self.px_ref = self.px_cur

#     def processFrame(self, frame_id):
#         self.px_ref, self.px_cur = featureTracking(self.last_frame, self.new_frame, self.px_ref)
#         E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp,
#                                        method=cv2.RANSAC, prob=0.99, threshold=1.0)
#         _, R, t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp=self.pp)
#         absolute_scale = self.getAbsoluteScale(frame_id)
#         if absolute_scale > 0.1:
#             self.cur_t = self.cur_t + self.cur_R.dot(t) * absolute_scale
#             self.cur_R = R.dot(self.cur_R)
#         if self.px_ref.shape[0] < kMinNumFeature:
#             # Phát hiện keypoints mới bằng ORB
#             keypoints = self.detector.detect(self.new_frame, None)
#             self.px_cur = np.array([kp.pt for kp in keypoints], dtype=np.float32)
#         self.px_ref = self.px_cur

#     def update(self, img, frame_id):
#         assert img.ndim == 2 and img.shape[0] == self.cam.height and img.shape[1] == self.cam.width, \
#             "Frame: provided image has not the same size as the camera model or image is not grayscale"
#         self.new_frame = img
#         if self.frame_stage == STAGE_DEFAULT_FRAME:
#             self.processFrame(frame_id)
#         elif self.frame_stage == STAGE_SECOND_FRAME:
#             self.processSecondFrame()
#         elif self.frame_stage == STAGE_FIRST_FRAME:
#             self.processFirstFrame()
#         self.last_frame = self.new_frame



import numpy as np 
import cv2

STAGE_FIRST_FRAME = 0
STAGE_SECOND_FRAME = 1
STAGE_DEFAULT_FRAME = 2
kMinNumFeature = 800 #1500

# Shi-Tomasi parameters
feature_params = dict(
    maxCorners= 1200, #1600
    qualityLevel=0.01,
    minDistance=5,
    blockSize=7
)

lk_params = dict(winSize  = (21, 21), 
				#maxLevel = 3,
             	criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

def featureTracking(image_ref, image_cur, px_ref):
	kp2, st, err = cv2.calcOpticalFlowPyrLK(image_ref, image_cur, px_ref, None, **lk_params)  #shape: [k,2] [k,1] [k,1]

	st = st.reshape(st.shape[0])
	kp1 = px_ref[st == 1]
	kp2 = kp2[st == 1]

	return kp1, kp2


class PinholeCamera:
	def __init__(self, width, height, fx, fy, cx, cy, 
				k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0):
		self.width = width
		self.height = height
		self.fx = fx
		self.fy = fy
		self.cx = cx
		self.cy = cy
		self.distortion = (abs(k1) > 0.0000001)
		self.d = [k1, k2, p1, p2, k3]


class VisualOdometry:
	def __init__(self, cam, annotations):
		self.frame_stage = 0
		self.cam = cam
		self.new_frame = None
		self.last_frame = None
		self.cur_R = None
		self.cur_t = None
		self.px_ref = None
		self.px_cur = None
		self.focal = cam.fx
		self.pp = (cam.cx, cam.cy)
		self.trueX, self.trueY, self.trueZ = 0, 0, 0
		self.detector = cv2.FastFeatureDetector_create(threshold=25, nonmaxSuppression=True)
		self.kfdetector = orb = cv2.ORB_create(
		    nfeatures=800,                          
		    scoreType=cv2.ORB_FAST_SCORE  # FAST_SCORE       
		)
		with open(annotations) as f:
			self.annotations = f.readlines()

	def getAbsoluteScale(self, frame_id):  #specialized for KITTI odometry dataset
		ss = self.annotations[frame_id-1].strip().split()
		x_prev = float(ss[3])
		y_prev = float(ss[7])
		z_prev = float(ss[11])
		ss = self.annotations[frame_id].strip().split()
		x = float(ss[3])
		y = float(ss[7])
		z = float(ss[11])
		self.trueX, self.trueY, self.trueZ = x, y, z
		return np.sqrt((x - x_prev)*(x - x_prev) + (y - y_prev)*(y - y_prev) + (z - z_prev)*(z - z_prev))

	def processFirstFrame(self):
		# self.px_ref = self.detector.detect(self.new_frame)
		self.px_ref = cv2.goodFeaturesToTrack(self.new_frame, mask=None, **feature_params)
		# self.px_ref = np.array([x.pt for x in self.px_ref], dtype=np.float32)
		self.frame_stage = STAGE_SECOND_FRAME

	def processSecondFrame(self):
		self.px_ref, self.px_cur = featureTracking(self.last_frame, self.new_frame, self.px_ref)
		E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp, method=cv2.RANSAC, prob=0.999, threshold=1.0)
		_, self.cur_R, self.cur_t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp = self.pp)
		self.frame_stage = STAGE_DEFAULT_FRAME 
		self.px_ref = self.px_cur

	def processFrame(self, frame_id):
		self.px_ref, self.px_cur = featureTracking(self.last_frame, self.new_frame, self.px_ref)
		E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp, method=cv2.RANSAC, prob=0.999, threshold=1.0)
		_, R, t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp = self.pp)
		absolute_scale = self.getAbsoluteScale(frame_id)
		if(absolute_scale > 0.1):
			self.cur_t = self.cur_t + absolute_scale*self.cur_R.dot(t) 
			self.cur_R = R.dot(self.cur_R)
		if(self.px_ref.shape[0] < kMinNumFeature):
			# self.px_cur = self.detector.detect(self.new_frame)
			# self.px_cur = np.array([x.pt for x in self.px_cur], dtype=np.float32)
			self.px_cur = cv2.goodFeaturesToTrack(self.new_frame, mask=None, **feature_params)
			
			a = self.kfdetector.detectAndCompute(self.new_frame, None)
		self.px_ref = self.px_cur

	def update(self, img, frame_id):
		assert(img.ndim==2 and img.shape[0]==self.cam.height and img.shape[1]==self.cam.width), "Frame: provided image has not the same size as the camera model or image is not grayscale"
		self.new_frame = img
		if(self.frame_stage == STAGE_DEFAULT_FRAME):
			self.processFrame(frame_id)
		elif(self.frame_stage == STAGE_SECOND_FRAME):
			self.processSecondFrame()
		elif(self.frame_stage == STAGE_FIRST_FRAME):
			self.processFirstFrame()
		self.last_frame = self.new_frame