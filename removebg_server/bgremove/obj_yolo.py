# from ultralytics import YOLO
# import cv2
# import numpy as np


# class BackgroundRemoval:
#     def __init__(self):
#         pass
#     # Function to perform post-processing on the binary mask
#     def post_process_mask(self, binary_mask):
#         # Perform morphological closing to fill small holes in the mask
#         kernel = np.ones((5, 5), np.uint8)
#         binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
#         return binary_mask

#     def remove_background(self):

#         model = YOLO('yolov8n-seg.pt')  # Use yolov8n-seg.pt for segmentation models

#         results = model.predict(source='bgremove/dataset')
#         for result in results:
#             # Create a dictionary to store masks for each class
#             class_masks = {}
#             for detection in result:
#                 class_name = detection.names[detection.boxes.cls.tolist().pop()]
#                 # Create a binary mask from detection
#                 binary_mask = np.zeros(result.orig_img.shape[:2], np.uint8)
#                 contour = detection.masks.xy.pop().astype(np.int32).reshape(-1, 1, 2)
#                 cv2.drawContours(binary_mask, [contour], -1, (255, 255, 255), cv2.FILLED)
#                 # Perform post-processing on the mask
#                 binary_mask = self.post_process_mask(binary_mask)
#                 # Add the mask to the dictionary for the corresponding class
#                 if class_name not in class_masks:
#                     class_masks[class_name] = binary_mask
#                 else:
#                     class_masks[class_name] += binary_mask

#             masked_image = cv2.bitwise_and(result.orig_img, result.orig_img, mask=class_masks['person'])
#             cv2.imwrite(f'bgremove/output/result.jpg', masked_image)
#             # Loop through the class masks and isolate objects
#             # for class_name, binary_mask in class_masks.items():
#             #     # Save the mask
#             #     # mask_filename = f'{class_name}_mask.jpg'
#             #     # cv2.imwrite(mask_filename, binary_mask)
#             #     # Isolate object with black background
#             #     masked_image = cv2.bitwise_and(result.orig_img, result.orig_img, mask=binary_mask)
#             #     cv2.imwrite(f'bgremove/output/{class_name}nobg.jpg', masked_image)


import cv2
import numpy as np
from ultralytics import YOLO


class BackgroundRemoval:
    @staticmethod
    def post_process_mask(binary_mask):
        # Perform morphological closing to fill small holes in the mask
        kernel = np.ones((5, 5), np.uint8)
        binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
        return binary_mask

    @staticmethod
    def remove_background():
        # Use yolov8n-seg.pt for segmentation models
        model = YOLO('yolov8n-seg.pt')

        results = model.predict(source='bgremove/dataset')
        for result in results:
            class_masks = {}
            for detection in result:
                class_name = detection.names[detection.boxes.cls.tolist(
                ).pop()]
                binary_mask = np.zeros(result.orig_img.shape[:2], np.uint8)
                contour = detection.masks.xy.pop().astype(np.int32).reshape(-1, 1, 2)
                cv2.drawContours(
                    binary_mask, [contour], -1, (255, 255, 255), cv2.FILLED)
                binary_mask = BackgroundRemoval.post_process_mask(binary_mask)
                if class_name not in class_masks:
                    class_masks[class_name] = binary_mask
                else:
                    class_masks[class_name] += binary_mask

            # Invert the mask to make background black and object white
            object_mask = 255 - class_masks['person']

            # Create a transparent image with the object and transparent background
            transparent_img = np.zeros_like(result.orig_img, np.uint8)
            # Set transparent image to black
            transparent_img[:] = (255, 255, 255)
            transparent_img = cv2.bitwise_and(
                transparent_img, transparent_img, mask=object_mask)

            # Combine the transparent object with the original image
            result_img = cv2.bitwise_and(
                result.orig_img, result.orig_img, mask=class_masks['person'])
            transparent_img += result_img
            
        cv2.imwrite(f'bgremove/output/result.jpg', transparent_img)
