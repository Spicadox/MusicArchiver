#!/usr/bin/env python
import os
import subprocess
import shutil
import sys


def downloadUpscale():
    # set current directory
    currentDirectory = input("Set Directory(if no value then default is cwd): ")

    if len(currentDirectory) == 0:
        currentDirectory = os.getcwd()

    # go to directory
    os.chdir(currentDirectory)

    # set waifu-caffe directory
    userWaifuDirectory = input("Waifu2x-Caffe Directory: ")
    waifuDirectory = userWaifuDirectory

    # set archive directory
    userArchiveDirectory = input("Archive File Directory(if no value then default is cwd): ")
    if len(userArchiveDirectory) == 0:
        userArchiveDirectory = os.getcwd() + "\\archive.txt"
    archiveDirectory = userArchiveDirectory

    # ask and set link if argv isn't specified
    if(len(sys.argv) < 2):
        link = input("URL: ")
    else:
        link = sys.argv[1]

    # check if there are more than 1 link
    if " " in link:
        url_list = link.split()
    else:
        url_list = [link]

    # run for all the urls in the list
    for url in url_list:

        # exit if its a playlist url
        if "playlist?list=" in url:
            print("Playlist archive not supported")
            break

        # get the full file name
        fullFileName = subprocess.run("youtube-dl --get-filename " + url, capture_output=True, text=True).stdout.strip("\n")
        fName = fullFileName.rsplit(".", 1)[0]

        opusFile = fName + ".opus"
        m4aFile = fName + ".m4a"
        mp3File = fName + ".mp3"

        # youtube-dlc arguments
        ytdlc_list = ['youtube-dl']
        ytdlc_list += ['--download-archive']
        ytdlc_list += [archiveDirectory]
        ytdlc_list += ['-f', 'bestaudio', '-x', '--add-metadata', '--write-thumbnail', url]

        # Run youtube-dlc to download url
        subprocess.run(ytdlc_list)

        # Set name of downloaded images
        pngFile = fName + ".png"
        webpFile = fName + ".webp"
        jpgFile = fName + ".jpg"

        # upscale image and add image cover
        for path, directories, files in os.walk(currentDirectory):
            # If webp or png exist
            if (any(x in files for x in [pngFile, webpFile, jpgFile])):
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

                # If webp or jpg image exists
                if(webpFile in files):
                    imageFile = webpFile
                elif(jpgFile in files):
                    imageFile = jpgFile
                else:
                    # If image file isn't webp or jpg
                    print("Unsupported image file")
                    break
                try:
                    # FFmpeg arguments list
                    ffmpeg_list = ['ffmpeg', '-i']
                    ffmpeg_list += [imageFile]
                    ffmpeg_list += ['-vf', 'scale=iw*min(1500/iw\,1500/ih):ih*min(1500/iw\,1500/ih),pad=1500:1500:(1500-iw)/2:(1500-ih)/2', 'temp.png']
                    # subprocess.run("ffmpeg -i " + webpFile + " -vf 'scale=iw*min(1500/iw\,1500/ih):ih*min(1500/iw\,1500/ih),pad=1500:1500:(1500-iw)/2:(1500-ih)/2' temp.png")
                    # subprocess.run("waifu2x-caffe-cui.exe -i temp.png -m noise_scale --scale_ratio 2 --noise_level 2 --tta 1 -p cudnn -o " + pngFile)
                    # subprocess.run("kid3-cli -c 'set picture:'temp.png' 'Album Cover'' " + fullAudioName)

                    subprocess.run(ffmpeg_list)

                    # Move the png to get upscaled
                    if os.path.isfile(waifuDirectory + "\\temp.png"):
                        os.remove(waifuDirectory + "\\temp.png")
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
                    os.remove(imageFile)
                    print("\nOperation Success")
                    break

                # on error remove files from the and undo operations
                except Exception:
                    print("Error")
                    if os.path.isfile(waifuDirectory + "\\temp.png"):
                        os.remove(waifuDirectory + "\\temp.png")
                    if os.path.isfile(currentDirectory + "\\temp.png"):
                        os.remove(currentDirectory + "\\temp.png")
                    if os.path.isfile(currentDirectory + "\\temp_2.png"):
                        os.remove(currentDirectory + "\\temp_2.png")
                    if os.path.isfile(waifuDirectory + "\\temp_2.png"):
                        os.remove(waifuDirectory + "\\temp_2.png")
                    if os.path.isfile(currentDirectory + "\\" + imageFile):
                        os.remove(currentDirectory + "\\" + imageFile)
                    if os.path.isfile(currentDirectory + "\\" + fullAudioName):
                        os.remove(currentDirectory + "\\" + fullAudioName)
                        # remove link from archive list
                        with open(archiveDirectory, "r+") as f:
                            lines = f.readlines()
                            lines = lines[:-1]
                            for line in lines:
                                f.write(line)

if __name__ == '__main__':
    repeat = ''
    doNotRepeat_list = ['n', 'no', 'No', 'N', 'NO']
    while(repeat not in doNotRepeat_list):
        downloadUpscale()
        repeat = input("\nWould you like to download again?(y/n): ")
