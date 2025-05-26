import cv2
import numpy as np
from ultralytics import YOLO


class Detect():
    def __init__(self, model_path=r"cv_model"):
        """
        Initialize YOLO detector with a given model path.
        """
        self.model = YOLO(model_path)

    def get_boxes(self, image):
        """
        Run YOLO on the image and return bounding boxes [x1, y1, x2, y2].
        """
        results = self.model(image)
        return [list(map(int, box[:4])) for box in results[0].boxes.xyxy.cpu().numpy()]

    def draw_boxes(self, image, boxes, color=(0, 255, 0), thickness=1):
        """
        Draws only bounding boxes on the image.
        """
        for x1, y1, x2, y2 in boxes:
            cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
        return image

    def detect_image_from_path(self, image_path, save_path="output.png"):
        """
        Detect objects in an image from path, draw boxes, and save output.
        """
        image = cv2.imread(image_path)
        boxes = self.get_boxes(image)
        image_with_boxes = self.draw_boxes(image, boxes)
        
        cv2.imwrite(save_path, image_with_boxes)
        return image_with_boxes

    def detect_image_from_array(self, image_array):
        """
        Detect objects in an image array and return array with boxes.
        """
        boxes = self.get_boxes(image_array)
        return self.draw_boxes(image_array, boxes)

    def detect_video_from_path(self, video_path, save_path="output.mp4"):
        """
        Run detection on video from file and save MP4 output with only boxes.
        """
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Save as MP4
        out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            boxes = self.get_boxes(frame)
            frame_with_boxes = self.draw_boxes(frame, boxes)
            out.write(frame_with_boxes)

        cap.release()
        out.release()


    def detect_video_from_stream(self, stream_source=0):
        """
        Run detection on webcam or stream input. Press 'q' to quit.
        """
        cap = cv2.VideoCapture(stream_source)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            boxes = self.get_boxes(frame)
            frame_with_boxes = self.draw_boxes(frame, boxes)

            cv2.imshow("YOLO Detection", frame_with_boxes)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    import numpy as np

    def generate_detection_heatmap(self, video_path, output_path=r"heatmap.jpg"):
        """
        Generate a heatmap of detection areas from a video using the YOLO model.
        Saves the heatmap as an image.
        """
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        heatmap = np.zeros((height, width), dtype=np.float32)

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            boxes = self.get_boxes(frame)

            for x1, y1, x2, y2 in boxes:
                heatmap[y1:y2, x1:x2] += 1

            frame_count += 1

        cap.release()

        # Normalise heatmap to 0-255 and apply color map
        normalized = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
        colored = cv2.applyColorMap(normalized.astype(np.uint8), cv2.COLORMAP_JET)

        cap = cv2.VideoCapture(video_path)
        ret, background = cap.read()
        cap.release()
        blended = cv2.addWeighted(background, 0.5, colored, 0.5, 0)
        cv2.imwrite(output_path, blended)

        print(f"Heatmap saved to {output_path}")