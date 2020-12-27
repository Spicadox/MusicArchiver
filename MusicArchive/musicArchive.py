import os
import subprocess
import shutil
import sys

def downloadUpscale():
    # set current directory
    # currentDirectory = "C:\\Users\\samph\\Videos\\FFMPEG VIDEO\\youtube_music_ download"
    currentDirectory = os.path.abspath("C:\\Users\\samph\\Videos\\FFMPEG VIDEO\\youtube_music_ download")

    # go to directory
    os.chdir(currentDirectory)

    # set waifu-caffe directory
    waifuDirectory = os.path.abspath("C:\\Users\\samph\\Documents\\waifu2x-caffe")

    # ask and set url if argv isn't specified
    if(len(sys.argv) < 2):
        url = input("URL: ")
    else:
        url = sys.argv[1]

    # get the full file name
    fullFileName = subprocess.run("youtube-dlc --get-filename " + url, capture_output=True, text=True).stdout.strip("\n")
    fName = fullFileName.rsplit(".", 1)[0]

    opusFile = fName + ".opus"
    m4aFile = fName + ".m4a"
    mp3File = fName + ".mp3"

    # Run youtube-dlc to download url
    subprocess.run("youtube-dlc -f bestaudio -x --add-metadata --write-thumbnail " + url)

    # Set name of downloaded images
    pngFile = fName + ".png"
    webpFile = fName + ".webp"

    # upscale image and add image cover
    for path, directories, files in os.walk(currentDirectory):
        # If webp or png exist
        if (any(x in files for x in [pngFile, webpFile])):
            # If opus, m4a, and worse case mp3 file exist
            if (opusFile in files):
                fullAudioName = opusFile
            elif (m4aFile in files):
                fullAudioName = m4aFile
            elif (mp3File in files):
                fullAudioName = mp3File
            else:
                # If audio file isn't opus or m4a
                print("Unsupported audio file")
                break

            # FFmpeg arguments list
            ffmpeg_list = ['ffmpeg', '-i']
            ffmpeg_list += [webpFile]
            ffmpeg_list += ['-vf', 'scale=iw*min(1500/iw\,1500/ih):ih*min(1500/iw\,1500/ih),pad=1500:1500:(1500-iw)/2:(1500-ih)/2', 'temp.png']
            # subprocess.run("ffmpeg -i " + webpFile + " -vf 'scale=iw*min(1500/iw\,1500/ih):ih*min(1500/iw\,1500/ih),pad=1500:1500:(1500-iw)/2:(1500-ih)/2' temp.png")
            # subprocess.run("waifu2x-caffe-cui.exe -i temp.png -m noise_scale --scale_ratio 2 --noise_level 2 --tta 1 -p cudnn -o " + pngFile)
            # subprocess.run("kid3-cli -c 'set picture:'temp.png' 'Album Cover'' " + fullAudioName)

            subprocess.run(ffmpeg_list)

            # Move the png to get upscaled
            shutil.move("temp.png", waifuDirectory)
            # Change directory to waifu2x-caffe-cui
            os.chdir(waifuDirectory)

            # Waifu2x-caffe arguments and run it
            waifu2x_list = ['waifu2x-caffe-cui.exe', '-i', 'temp.png', '-m', 'noise_scale', '--scale_ratio', '2', '--noise_level', '2', '--tta', '1', '-p', 'cudnn', '-o', 'temp_2.png']
            subprocess.run(waifu2x_list)

            # Change directory and move upscaled image back to original directory and remove original png
            shutil.move("temp_2.png", currentDirectory)
            os.remove("temp.png")
            os.chdir(currentDirectory)

            # Kids3-cli arguments and run it to add image cover
            kids3_list = ['kid3-cli', '-c', "set picture:temp_2.png 'Album Cover'"]
            kids3_list += [fullAudioName]
            subprocess.run(kids3_list)

            # Remove all image files and exit
            os.remove("temp_2.png")
            os.remove(webpFile)
            print("Exited Successfully")
            break
        else:
            print("Error, Can't Find Image\n Exiting")
            break


if __name__ == '__main__':
    downloadUpscale()
