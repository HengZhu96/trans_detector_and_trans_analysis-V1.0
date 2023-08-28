# yolo+deepsort trans detector and trans analysis V1.0
This project mainly implements video-based traffic data statistics, such as the number of vehicles passing through different detection areas and the elapsed time (only one record per pass), and supports customizing any number of detection areas at any location.

If you have any questions on this project, please contact me without any hesitation (Both English and Chinese are ok).

- Custom detection area can be realized by mouse.
- Default detection type: person, bicycle, car, motorcycle, bus, truck.
- The test results can be output to csv, currently output type, id, detection area index, and object elapsed time.


## Custom detection areas sample

- The green rectangles are the custom detection area which are drawn with the left mouse button.
![sample_of_draw_detection_area.png](pic_sample%2Fsample_of_draw_detection_area.png)

## Running sample
- The blue area in the figure is the detection area drawn in the previous step.
![sample_of_running.png](pic_sample%2Fsample_of_running.png)

## Result sample
![sample_of_csv_result.png](pic_sample%2Fsample_of_csv_result.png)

## Environment

- python 3.8，pip 20+
- pytorch (Advise a GPU vision，if you have a GPU.)
- pip install -r requirements.txt

## How to run

- Make sure that the torch and torchvison versions are installed correctly, this step may take a while.
- Change line 18 in main.py to your desired output name.
- Change line 66 and line 124 in main.py to the video address you need to analyze.

## Structure Used

- https://github.com/Sharpiless/Yolov5-deepsort-inference
- https://github.com/ultralytics/yolov5/
- https://github.com/ZQPei/deep_sort_pytorch
