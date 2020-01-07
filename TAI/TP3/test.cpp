#include <opencv2/core/core.hpp>


int main(void){

    cv::Mat image = cv::imread("./ImgCondComp/orl_faces/s01/01.pgm", CV_LOAD_IMAGE_GRAYSCALE);
    cv::Mat dst;
    cv::resize(image, dst, cv::Size(150,150));

    return 0;
}