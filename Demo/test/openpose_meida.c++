#include "Demo/test/openpose/headers.hpp"

int main(int argc, char** argv)
{
    // OpenPose 초기화
    op::Wrapper opWrapper;
    opWrapper.configure(op::WrapperStructPose{});

    // 입력 동영상 파일 경로
    const std::string videoPath = "F:/backup/Project/CapStone/code/Demo/data/color_output.mp4";

    // 입력 동영상 캡처
    cv::VideoCapture videoCapture(videoPath);

    // 캡처된 첫 프레임 가져오기
    cv::Mat frame;
    videoCapture >> frame;

    // 프레임 크기 설정
    const auto frameWidth = frame.cols;
    const auto frameHeight = frame.rows;

    // OpenPose 입력 프레임 크기 설정
    opWrapper.updateResolution({ frameWidth, frameHeight });

    // OpenPose 시작
    opWrapper.start();

    // 동영상 프레임 단위로 처리
    while (true)
    {
        // 프레임 캡처
        videoCapture >> frame;

        // 동영상이 끝나면 종료
        if (frame.empty())
            break;

        // OpenPose에 프레임 전달
        op::Array<float> outputArray;
        opWrapper.emplaceAndPop([&](cv::Mat& input) -> void
        {
            input = frame;
            cv::cvtColor(input, input, cv::COLOR_BGR2RGB);
        });

        // 스켈레톤 추출 결과 가져오기
        const auto& datum = opWrapper.getPoseKeypoints();
        const auto& poseKeypoints = datum.getConstCvMat();

        // 스켈레톤 그리기
        for (int i = 0; i < poseKeypoints.rows; i++)
        {
            const auto* keypointsPtr = poseKeypoints.ptr<float>(i);
            for (int j = 0; j < poseKeypoints.cols; j += 3)
            {
                const auto keypointX = keypointsPtr[j];
                const auto keypointY = keypointsPtr[j + 1];
                const auto keypointScore = keypointsPtr[j + 2];

                if (keypointScore > 0.1)
                {
                    // 스켈레톤 점 그리기
                    cv::circle(frame, cv::Point2f(keypointX, keypointY), 3, cv::Scalar(0, 255, 0), -1);
                }
            }
        }

        // 화면에 결과 프레임 표시
        cv::imshow("OpenPose Skeleton", frame);

        // ESC 키로 종료
        if (cv::waitKey(1) == 27)
            break;
    }

    // OpenPose 정지
    opWrapper.stop();

    // 창 닫기
    cv::destroyAllWindows();

    return 0;
}
