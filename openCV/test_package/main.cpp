#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>

using namespace cv;

int main(int argc, char** argv )
{
	CvCapture* capture = cvCaptureFromCAM( CV_CAP_DSHOW );
    if( capture == nullptr)
        return 1;
	
	return 0;
}
