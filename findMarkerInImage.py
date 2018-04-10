import cv2
import MarkerTracker
import math

### Constants ###########
order_of_marker_input = 12
size_of_kernel_input = 30
path_to_image = '/home/blaise/Desktop/MSc/2_sem_robotics/gitRepo/marker_tracking/marker_tracking/media/pic2.jpg'
#path_to_image = '/media/pic1.jpg'
path_to_vid = '/media/vid1.jpg'
track_orientation = False

def annotate_frame_with_detected_marker(frame, marker_pose, order_of_marker_input, size_of_kernel_input,
                                        track_orientation):
    line_width_of_circle = 20
    if marker_pose.quality > 0.5:
        marker_color = (0, 255, 0)
    else:
        marker_color = (255, 0, 255)
    cv2.circle(frame, (marker_pose.x, marker_pose.y), int(size_of_kernel_input / 2),
               marker_color, line_width_of_circle)

    dist = 50
    direction_line_width = 1
    if track_orientation:
        # Mark the orientation of the detected marker
        point1 = (marker_pose.x, marker_pose.y)
        point2 = (math.trunc(marker_pose.x + dist * math.cos(marker_pose.theta)),
                  math.trunc(marker_pose.y + dist * math.sin(marker_pose.theta)))

        cv2.line(frame, point1, point2, marker_color, direction_line_width)
    else:
        point1 = (marker_pose.x, marker_pose.y)
        theta = marker_pose.theta
        for k in range(order_of_marker_input):
            theta += 2 * math.pi / order_of_marker_input
            point2 = (math.trunc(marker_pose.x + dist * math.cos(theta)),
                      math.trunc(marker_pose.y + dist * math.sin(theta)))

            cv2.line(frame, point1, point2, marker_color, direction_line_width)

def main():
    image = cv2.imread(path_to_image,0)
    tracker = MarkerTracker.MarkerTracker(order_of_marker_input,
                                          size_of_kernel_input, 1.0)

    tracker.track_marker_with_missing_black_leg = track_orientation

    marker_pose = tracker.locate_marker(image)

    
    annotate_frame_with_detected_marker(image,marker_pose,
                                        order_of_marker_input,
                                        size_of_kernel_input,
                                        track_orientation)
    
    '''
    norm_image = cv2.normalize(tracker.frame_sum_squared,None,aplha=0,
                               beta=1,norm_type=cv2.NORM_MINMAX,
                               dtype=cv2.CV_32F)
   
    
    cv2.imshow('Response',norm_image)
    '''
    print(marker_pose)
    cv2.imshow('Image',image)   
    cv2.imwrite('/home/blaise/Desktop/MSc/2_sem_robotics/gitRepo/marker_tracking/MarkerLocator/media/pic1_tracked.jpg', image)    

if __name__ == '__main__':
    main()
