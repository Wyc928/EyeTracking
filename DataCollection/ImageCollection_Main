/*
	Author: Wenyu
  Modified by Wang Yongchen
	Version: 1.0
	Date: 3/11/2019
	Dependencies: VS2015, OpenCV3.1.0, boost1.69.0
	Function:
	v2.0 collect image from Logitech CE1000
*/

#include <iostream>
#include <fstream>
#include <opencv2\opencv.hpp>
#include "gazeapi.h"
//add by wangyongchen
#include <time.h>
#include<string>
#include<sys/timeb.h>
#include<Windows.h>

#define FRAME_WIDTH 1920
#define FRAME_HEIGHT 1080

using namespace cv;
using namespace std;

VideoCapture camera;

struct GazePoint {
	double x;
	double y;
}my_gaze_data;

//add by wangyongchen
struct NowDate
{
	char date[16]; 
	char time[16]; 
	char millitm[4];  
};
// --- MyGaze definition
class MyGaze : public gtl::IGazeListener
{
public:
	MyGaze();
	~MyGaze();
private:
	// IGazeListener
	void on_gaze_data(gtl::GazeData const & gaze_data);
private:
	gtl::GazeApi m_api;
};

// --- MyGaze implementation
MyGaze::MyGaze()
	: m_api(0) // verbose_level 0 (disabled)
{
	// Connect to the server on the default TCP port (6555)
	std::cout << "Connect..." << std::endl;
	if (m_api.connect())
	{
		// Enable GazeData notifications
		std::cout << "Connect Success" << std::endl;
		m_api.add_listener(*this);
	}
	gtl::ServerState gs = m_api.update_server_state();
}

MyGaze::~MyGaze()
{
	m_api.remove_listener(*this);
	m_api.disconnect();
}

void MyGaze::on_gaze_data(gtl::GazeData const & gaze_data)
{
	//std::cout << "#" << std::endl;
	if (gaze_data.state & gtl::GazeData::GD_STATE_TRACKING_GAZE)
	{
		gtl::Point2D const & smoothedCoordinates = gaze_data.avg;
		// Move GUI point, do hit-testing, log coordinates, etc.
		std::cout << smoothedCoordinates.x << " " << smoothedCoordinates.y << std::endl;
		//::SetCursorPos(smoothedCoordinates.x, smoothedCoordinates.y);
		my_gaze_data = { smoothedCoordinates.x, smoothedCoordinates.y};
	}
}



int main() {
	// init record info
	int frame_index = 0;
	//std::ofstream gaze_file("gazeData.txt");
	//add by wangyongchen
	//std::ofstream frame_time("frameTime.txt");
	//MyGaze my_gaze;
	// init camera
	camera.open(0);
	camera.set(CV_CAP_PROP_FRAME_WIDTH, FRAME_WIDTH);
	camera.set(CV_CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT);
	Mat frame;
	bool running = true;
	while (running == true) {
		camera >> frame;
		if (!frame.empty()) {
			char file_name[255] = "";
			sprintf(file_name, "F:\\DataSet\\Data\\IMAGE\\%d.bmp", frame_index);
			imwrite(file_name, frame);
			cout << file_name << endl;
			
			if (frame_index == 499) {// push esc to quit
				running = false;
				LPCWSTR content = L"Finish";
				LPCWSTR title = L"Alert";
				MessageBox(NULL, content, title, MB_SYSTEMMODAL);
				break;
			}
			frame_index++;
		}
	}
	camera.release();
	return 0;
}
