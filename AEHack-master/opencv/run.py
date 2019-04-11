import detect_utils as du

filename = "images/plane0.avi"
window_size = 5

if __name__ == "__main__":
	du.localize_video(filename, window_size)
