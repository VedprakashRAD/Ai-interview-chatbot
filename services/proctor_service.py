import cv2
import numpy as np
from deepface import DeepFace
import mediapipe as mp
import threading
import time
from datetime import datetime
import os

class ProctorService:
    def __init__(self):
        self.warning_count = 0
        self.MAX_WARNINGS = 3
        self.reference_image = None
        self.is_active = False
        self.cameras = []
        self.frames = []
        
        # Initialize MediaPipe solutions
        self.mp_face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5
        )
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_pose = mp.solutions.pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.snapshots_dir = "uploads/snapshots"
        os.makedirs(self.snapshots_dir, exist_ok=True)
        
        # Store previous face landmarks for movement detection
        self.prev_landmarks = None
        self.movement_threshold = 0.1
        
    def initialize_cameras(self):
        """Initialize both cameras"""
        try:
            # Try to open both cameras
            self.cameras = [cv2.VideoCapture(0), cv2.VideoCapture(1)]
            if not all(cam.isOpened() for cam in self.cameras):
                raise ValueError("Failed to open both cameras")
            return True
        except Exception as e:
            print(f"Camera initialization error: {str(e)}")
            return False

    def start_proctoring(self, candidate_id: str):
        """Start the proctoring session"""
        if self.is_active:
            return False
            
        self.is_active = True
        self.warning_count = 0
        
        # Start monitoring threads
        threading.Thread(target=self._monitor_cameras, args=(candidate_id,)).start()
        threading.Thread(target=self._analyze_behavior).start()
        return True

    def stop_proctoring(self):
        """Stop the proctoring session"""
        self.is_active = False
        for cam in self.cameras:
            cam.release()
        cv2.destroyAllWindows()

    def set_reference_image(self, image):
        """Set the reference image for identity verification"""
        self.reference_image = image

    def _monitor_cameras(self, candidate_id: str):
        """Monitor both cameras continuously"""
        while self.is_active:
            self.frames = []
            for i, cam in enumerate(self.cameras):
                ret, frame = cam.read()
                if not ret:
                    self._handle_camera_failure()
                    return
                self.frames.append(frame)
                
            # Take periodic snapshots
            if time.time() % 30 == 0:  # Every 30 seconds
                self._save_snapshot(self.frames[0], candidate_id)

    def _analyze_behavior(self):
        """Analyze candidate behavior in real-time"""
        while self.is_active and self.frames:
            try:
                main_frame = self.frames[0]
                rgb_frame = cv2.cvtColor(main_frame, cv2.COLOR_BGR2RGB)
                
                # Detect faces
                face_results = self.mp_face_detection.process(rgb_frame)
                if face_results.detections:
                    # Count number of faces
                    if len(face_results.detections) > 1:
                        self._issue_warning("Multiple people detected")
                    
                    # Check face mesh for movement
                    mesh_results = self.mp_face_mesh.process(rgb_frame)
                    if mesh_results.multi_face_landmarks:
                        current_landmarks = mesh_results.multi_face_landmarks[0]
                        if self._detect_excessive_movement(current_landmarks):
                            self._issue_warning("Excessive head movement detected")
                        self.prev_landmarks = current_landmarks
                else:
                    self._issue_warning("No face detected")
                
                # Check body pose for suspicious movements
                pose_results = self.mp_pose.process(rgb_frame)
                if pose_results.pose_landmarks:
                    if self._detect_suspicious_pose(pose_results.pose_landmarks):
                        self._issue_warning("Suspicious pose detected")
                
            except Exception as e:
                print(f"Analysis error: {str(e)}")
            
            time.sleep(0.1)  # Reduce CPU usage

    def _detect_excessive_movement(self, current_landmarks):
        """Detect if there's excessive head movement"""
        if self.prev_landmarks is None:
            return False
            
        movement = 0
        for i in range(len(current_landmarks.landmark)):
            curr = current_landmarks.landmark[i]
            prev = self.prev_landmarks.landmark[i]
            movement += abs(curr.x - prev.x) + abs(curr.y - prev.y)
            
        avg_movement = movement / len(current_landmarks.landmark)
        return avg_movement > self.movement_threshold

    def _detect_suspicious_pose(self, pose_landmarks):
        """Detect suspicious body movements"""
        # Get key points
        nose = pose_landmarks.landmark[0]
        left_ear = pose_landmarks.landmark[7]
        right_ear = pose_landmarks.landmark[8]
        
        # Check if head is turned too far
        head_rotation = abs(left_ear.x - right_ear.x)
        if head_rotation > 0.3:  # Threshold for head rotation
            return True
            
        # Check if looking down
        if nose.y > 0.7:  # Threshold for looking down
            return True
            
        return False

    def _verify_identity(self, current_frame):
        """Verify if the current person matches the reference image"""
        try:
            result = DeepFace.verify(
                img1_path=self.reference_image,
                img2_path=current_frame,
                enforce_detection=False
            )
            return result['verified']
        except:
            return False

    def _save_snapshot(self, frame, candidate_id: str):
        """Save a snapshot of the candidate"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.snapshots_dir}/{candidate_id}_{timestamp}.jpg"
        cv2.imwrite(filename, frame)

    def _issue_warning(self, reason: str):
        """Issue a warning to the candidate"""
        self.warning_count += 1
        if self.warning_count >= self.MAX_WARNINGS:
            self._auto_submit()
        return {
            "warning_count": self.warning_count,
            "reason": reason,
            "max_warnings": self.MAX_WARNINGS
        }

    def _handle_camera_failure(self):
        """Handle camera failure by auto-submitting"""
        self._auto_submit()

    def _auto_submit(self):
        """Auto-submit the test"""
        self.stop_proctoring()
        # Implement test submission logic here
        return {
            "status": "auto_submitted",
            "message": "Test auto-submitted due to multiple violations. Please contact test admin."
        } 