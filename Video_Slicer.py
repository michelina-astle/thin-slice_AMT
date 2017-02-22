__author__ = 'mmadaio'
import time

def write_slice_bat_file():

    filepath = "C:\Users\\articulab.rae\Desktop" ## Change to your local filepath where the Batch# folder is
    input_batch_folder = filepath + "\Batch5\\"  ## Change to be whichever batch you're on
    dyad = ["D15_S2", "D16_S1", "D17_S2"]  ## Change these to your video files
    length_of_video_in_slices = [112, 106, 115]   ## Change these to be the length of your video, in 30-second slices

    filename = "video_slicer.bat"   ## This is the name of the file created by running this script
    text = []

    for k in range(len(dyad)):
        print k
        j = dyad[k]
        print j
        input_file = j + "_Both.mp4"   ## Change this to the end of your video files
        output_slice_folder = input_batch_folder + "Slices" + "\\" + j + "\\"

        current = 0
        increment = 30
        text.append("mkdir " + output_slice_folder + "\n \n")
        for i in range(length_of_video_in_slices[k]):
            print i
            current = current + increment
            print current
            current_time = time.strftime("%H:%M:%S", time.gmtime(current))
            print current_time

            output_file = j + "_Both_Slice_{0}.mp4".format(i)  ## Change to .wmv if necessary
            print output_file
            text.append("ffmpeg -i " + input_batch_folder + input_file + " -ss {0} -t 00:00:30 -strict -2 ".format(current_time) + output_slice_folder + output_file + "\n \n")
    output = "".join(text)
    print output
    batch_output = open(filename, "w")

    batch_output.write(output)
    batch_output.close()

write_slice_bat_file()