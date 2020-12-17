# ComputerVision-FingerPaint-Pygame
Drawing with fingers Enabled by pure Image Processing or ML, and using the drawn data to play a game built with pytorch

The idea of the this project is to draw shapes using your hands, and when the shapes are drawn correctly, objects with matching symbols will explode, gamifying the experience.


There are 2 approaches i tried at the beginning, the first of all was a pure Image processing solution.
Where i would segment the hand using Color channels, (i also tried taking a snapshot of the background and subtracting it each frame, check the master branch).
then after the color segmentation, i would detect the biggest contour and using it i would obtain the convex hull.
and tracking the points corresponding to the index finger and the middle finger i was able to draw in the air!

Image Processing Solution Result:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/O0KwbtfEN0w/0.jpg)](https://youtu.be/O0KwbtfEN0w)

But due to the inconsistency of the image processing solution , i decided to use a Deep learning solution.

i used the mediapipe solution provdied by google and reached this result:

(..Insert Image..)

so i decided to continue using it.
