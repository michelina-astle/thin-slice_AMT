__author__ = 'mmadaio'
import time

def write_slice_bat_file():

    filepath = "C:\Users\\articulab.interns\Desktop\RAPT_WoZ_Videos\\" ## Change to your local filepath where the video file folder is
    participant = ["P1", "P2", "P3", "P4", ""]  ## Change these to the start of the video file names ********* DO THIS*********
    length_of_video_in_slices = [112, 106, 115]   ## Change these to be the length of each video, in 30-second slices. Be sure to put these in the order of the participant numbers above

    filename = "video_slicer.bat"   ## This is the name of the file created by running this script
    text = []

    for k in range(len(participant)):
        print k
        j = participant[k]
        print j
        input_file = j + ".mp4"   ## Change this to the end of your video files (should be just .mp4)
        output_slice_folder = filepath + "Slices\\" #+ "\\" + j + "\\"
        print output_slice_folder
        current = 0
        increment = 30
        text.append("mkdir " + output_slice_folder + "\n \n")
        for i in range(1): #length_of_video_in_slices[k]):
            print i
            print current
            current_time = time.strftime("%H:%M:%S", time.gmtime(current))
            print current_time

            output_file = j + "_Slice_{0}.mp4".format(i)  ## Change to .wmv if necessary
            print output_file
            text.append("ffmpeg -i " + filepath + input_file + " -ss {0} -t 00:00:30 -strict -2 ".format(current_time) + output_slice_folder + output_file + "\n \n")
            current = current + increment

    output = "".join(text)
    print output
    batch_output = open(filename, "w")

    batch_output.write(output)
    batch_output.close()

write_slice_bat_file()