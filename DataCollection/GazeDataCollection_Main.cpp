/*
	Author: Wenyu
  Modified by Wang Yongchen
	Version: 1.0
	Date: 3/11/2019
	Dependencies: VS2015, OpenCV3.1.0, boost1.69.0
	Function:
	v2.0 collect gaze data from TheEyeTribe
*/

#include <iostream>
#include <fstream>
#include <opencv2\opencv.hpp>
#include "gazeapi.h"
//add by wangyongchen
#include <time.h>
#include<string>
#include<sys/timeb.h>

#define FRAME_WIDTH 1920
#define FRAME_HEIGHT 1080
#define OUTPUT_FILE "F:\\DataSet\\Data\\GazeData\\GazeOriginalData.txt"

using namespace cv;
using namespace std;

VideoCapture camera;

struct GazePoint {
	double x;
	double y;
}my_gaze_data;

//add by wangyongchen
int frame_index = 0;

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
	void output_gaze_data(GazePoint gaze_data);
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
	if (gaze_data.state & gtl::GazeData::GD_STATE_TRACKING_GAZE)
	{
		gtl::Point2D const & smoothedCoordinates = gaze_data.avg;
		// Move GUI point, do hit-testing, log coordinates, etc.
		std::cout << smoothedCoordinates.x << " " << smoothedCoordinates.y << std::endl;

		my_gaze_data = { smoothedCoordinates.x, smoothedCoordinates.y};
		output_gaze_data(my_gaze_data);
	}
	if (waitKey(0) == 27)
		exit(0);
}
//add by wangyongchen
void MyGaze::output_gaze_data(GazePoint gaze_data)
{
	std::ofstream gaze_file(OUTPUT_FILE,ios::app);
	int gaze_point_x = int(my_gaze_data.x);
	int gaze_point_y = int(my_gaze_data.y);

	time_t timep;
	time(&timep);
	struct timeb tb;
	ftime(&tb);
	char millitm[16];
	sprintf(millitm, "%d", tb.millitm);
	string str_millitm;
	str_millitm = string(millitm);
	int strlen = str_millitm.length();
	if (strlen < 3) {
		for (int cnt = 0; cnt < 3 - strlen; cnt++) {
			str_millitm = "0" + str_millitm;
		}
	}
	str_millitm = "." + str_millitm;
	gaze_file << frame_index << "\t" << gaze_point_x << "\t" << gaze_point_y << "\t" << timep << str_millitm << std::endl;
	gaze_file.close();
	frame_index++;
}


int main() {
	// init record info
	frame_index = 0;
	MyGaze my_gaze;
	if (remove(OUTPUT_FILE) == 0) {
		cout << "删除成功" << endl;
	}
	else {
		cout << "删除失败" << endl;
	}
	while (true) {
		
		if (waitKey(100) == 27)
			break;
	}
	//camera.release();
	return 0;
}
