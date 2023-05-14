import cv2
import time

#img x,y좌표에 text 표시
def draw_text(img,text,x,y):
    font  = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_color = (255,0,0)
    text_color_bg = (0,0,0)
    
    text_size, _ = cv2.getTextSize(text,font,font_scale,font_thickness)
    text_w, text_h = text_size
    offset = 5
    
    cv2.rectangle(img,(x-offset,y-offset),(x+text_w+offset,y+text_h+offset), text_color_bg,-1)
    cv2.putText(img,text,(x,y+text_h+font_scale-1),font,font_scale,text_color,font_thickness)

def ShowFPS(frame, last_time, time_per_frame_video):
    time_per_frame = time.perf_counter() - last_time
    time_sleep_frame = max(0, time_per_frame_video - time_per_frame)
    time.sleep(time_sleep_frame)
    
    real_fps = 1/(time.perf_counter()-last_time)
    last_time = time.perf_counter()
    
    text = "%.2f fps" % real_fps
    
    draw_text(frame,text,30,50)
    
